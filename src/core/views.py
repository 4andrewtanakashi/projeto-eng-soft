from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.db.models import ProtectedError, Q

from django.views.generic import ListView, FormView
from .models import Propriedade, Reserva, Pagamento
from .forms import *
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
import datetime
import time
from django.contrib import messages


# Classe de controle que exibe as propriedades
# De um usuário na tela
class MinhasPropriedades(ListView):
    model = Propriedade
    template_name = 'core/minhaspropriedades.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Minhas propriedades'
        return context

    def get_queryset(self):
        return Propriedade.objects.filter(proprietario=self.request.user)

# Classe de controle que exibe todas as propriedades
# Que estão disponíveis de acordo com uma cidade, uma data inicial
# E uma data final
class PropDisponiveis(ListView):
    model = Propriedade
    template_name = 'core/propriedades.html'
    

    def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['titulo'] = 'Resultados da busca'
            context['ini'] = self.kwargs['ini']
            context['fim'] = self.kwargs['fim']
            return context

    def get_queryset(self):
        data_ini = datetime.datetime.strptime(self.kwargs['ini'],'%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(self.kwargs['fim'],'%Y-%m-%d').date()

        prop = Propriedade.objects.filter(cidade__icontains=self.kwargs['cidade'])

        reservas = Reserva.objects.filter(propriedade__in=prop).filter(
            Q(dini__lte=data_fim, dfim__gte=data_ini)
        )

        prop = prop.exclude(id__in=reservas.values_list('propriedade', flat=True))

        return prop

# Classe de controle que exibe todas as reservas
# De um usuário na tela
class MinhasReservas(ListView):
    model = Reserva
    template_name = 'core/minhasreservas.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Minhas reservas'
        return context

    def get_queryset(self):
        return Reserva.objects.filter(hospede=self.request.user)

# Função de controle que exibe os detalhes de uma propriedade
# Específica na tela, sendo que essa propriedade é determinada
# Pela chave primária
def prop_detalhe_view(request, pk):
    propriedade = get_object_or_404(Propriedade, id=pk)
    reservas = Reserva.objects.all().filter(propriedade=propriedade)
    dados = []
    for reserva in reservas:
        hospede = reserva.hospede
        data_ini = reserva.dini.strftime('%Y-%m-%d')
        data_fim = reserva.dfim.strftime('%Y-%m-%d')
        dados.append((hospede, data_ini, data_fim))

    return render(request, 'core/propriedade.html', context={'prop': propriedade, 'user': request.user, 'dados': dados})

# Função de controle que exibe os detalhes de uma propriedade
# Específica na tela, porém no contexto de efetuar a reserva
# Nesse caso, além da chave primária tanto a data inicial
# Quanto a data final estarão no contexto da visão
# A fim de determinar se é possível efetuar a reserva
def prop_detalhe_reserva_view(request, pk, ini, fim):
    propriedade = get_object_or_404(Propriedade, id=pk)
    datas = []
    reservas = Reserva.objects.all().filter(propriedade=propriedade)
    data_ini = None
    data_fim = None
    for reserva in reservas:
        data_ini = reserva.dini.strftime('%Y-%m-%d')
        data_fim = reserva.dfim.strftime('%Y-%m-%d')
        datas.append((data_ini, data_fim))
    return render(request, 'core/propriedade.html', context={'prop': propriedade, 'user': request.user, 'ini': ini, 'fim': fim, 'datas': datas})

# Função de controle que exibe os detalhes de uma reserva
# Específica na tela
# A reserva é dependente da chave primária, e o controle envia de contexto
# Uma variável booleana que controla se a reserva é editável ou não
def reserva_detalhe_view(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)
    pode_editar = True
    if (reserva.dini < datetime.date.today() or reserva.dfim < datetime.date.today()):
        pode_editar = False
    return render(request, 'core/reserva.html', context={'reserva': reserva, 'user': request.user, 'editavel': pode_editar})

# Função de controle que exibe um formulário
# Para cadastrar uma propriedade no sistema
def add_propriedade_view(request): 
    form = PropriedadeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        propriedade = form.save(commit=False)
        propriedade.proprietario = request.user  # use your own profile here
        propriedade.save()
        return redirect('/accounts/propriedades/')
    return render(request, 'core/form_propriedade.html', {'form': form}) 

# Função de controle que trata a exclusão
# De uma propriedade no sistema
# Caso não seja possível excluir, uma mensagem de erro
# É enviada por meio do objeto messages
def apagar_propriedade_view(request, pk):
    propriedade = get_object_or_404(Propriedade, pk=pk)
    try:
        propriedade.delete()
        return redirect('/accounts/propriedades/')
    except ProtectedError as e:
        messages.error(request, 'Não foi possível remover a propriedade, pois ela já possui reservas.')
        return redirect('/propriedade/' + str(pk))

# Função de controle que exibe um formulário
# Para editar uma propriedade já existente no sistema
def edit_propriedade_view(request, pk): 
    instance = get_object_or_404(Propriedade, id=pk)
    form = PropriedadeEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/accounts/propriedades/')
    return render(request, 'core/form_edit_propriedade.html', {'form': form}) 

# Função de controle que exibe um formulário
# Para adicionar uma reserva no sistema
def add_reserva_view(request, pk, ini, fim):
    propriedade = get_object_or_404(Propriedade, id=pk)
    nome = propriedade.nome

    form = ReservaForm(request.POST or None, initial = {'dini': ini, 'dfim': fim, 'qtd_pessoas': 1, 'propriedade': propriedade})
    formPagamento = PagamentoForm(request.POST or None)

    if form.is_valid() and formPagamento.is_valid():
        reserva = form.save(commit=False)
        reserva.hospede = request.user
        reserva.propriedade = propriedade
        reserva.propriedade.save()
        pagamento = formPagamento.save()
        reserva.dados_pagamento = pagamento
        reserva.save()
        return redirect('/accounts/reservas/')
    return render(request, 'core/form_reserva.html', {'form': form, 'form_pag': formPagamento, 'nome': nome}) 

# Função de controle que exibe um formulário
# Para editar uma reserva já existente no sistema
def edit_reserva_view(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)
    form = ReservaEditForm(request.POST or None, instance=reserva)
    form_pag = PagamentoEditForm(request.POST or None)
    if form.is_valid() and form_pag.is_valid():
        form.save()
        form_pag.save()
        return redirect('/reserva/' + str(pk))
    return render(request, 'core/form_edit_reserva.html', {'form': form, 'form_pag': form_pag}) 

# Função de controle que trata a exclusão
# De uma reserva no sistema
# Caso não seja possível excluir, uma mensagem de erro
# É enviada por meio do objeto messages
def apagar_reserva_view(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if (reserva.dini < datetime.date.today() or reserva.dfim < datetime.date.today()):
        messages.error(request, 'Não foi possível remover a reserva pois ela já ocorreu.')
        return redirect('/reserva/' + str(pk) + '/')
    try:
        pagamento = reserva.dados_pagamento
        reserva.delete()
        pagamento.delete()
        return redirect('/accounts/reservas/')
    except ProtectedError as e:
        messages.error(request, 'Não foi possível remover a reserva.')
        return redirect('/reserva/' + str(pk) + '/')

# Uma função de controle
# Que trata a exibição da tela inicial do sistema
def index_view(request):
    form = BuscaPropForm(request.POST or None)
    if (form.is_valid()):
        ini = form.cleaned_data['data_ini'].strftime('%Y-%m-%d')
        fim = form.cleaned_data['data_fim'].strftime('%Y-%m-%d')
        cidade = form.cleaned_data['cidade']
        return HttpResponseRedirect('/propriedades/'+ cidade +'/' + ini + '/' + fim)
    return render(request,'core/index.html', {'form': form})

# Uma função de controle que exibe um formulário
# Para que o usuário possa se autenticar no sistema
def signup_view(request):
    form = RegistrarForm(request.POST or None)

    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    context = {'form': form}
    return render(request, 'core/signup.html', context)

# Uma função de controle que exibe os dados de um usuário
# Na tela
def usuario_view(request):
    qtd_propriedades = Propriedade.objects.all().filter(proprietario=request.user).count()
    qtd_reservas = Reserva.objects.all().filter(hospede=request.user).count()

    usuario = request.user
    context = {'user': request.user, 'qtd': qtd_propriedades, 'qtdr': qtd_reservas}
    return render(request, 'core/user.html', context)

# Função de controle que exibe um formulário para que o usuário
# Possa atualizar seus dados cadastrais
def edit_usuario_view(request):
    form = AtualizarUsuarioForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('/accounts/')
    return render(request, 'core/form_edit_user.html', {'form': form})