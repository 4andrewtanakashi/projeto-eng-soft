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


# Create your views here.

class MinhasPropriedades(ListView):
    model = Propriedade
    template_name = 'core/minhaspropriedades.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Minhas propriedades'
        return context

    def get_queryset(self):
        return Propriedade.objects.filter(proprietario=self.request.user)

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

        # reservas = Reserva.objects.filter(propriedade__in=prop).filter(
        #     Q(ini__lte=data_ini, fim__gte=data_fim) | # ok
        #     Q(ini__gt=data_ini, fim__gt=data_fim, fim__gt=data_ini)| 
        #     Q(ini__lt=data_ini, fim__lt=data_fim, fim__gt=data_ini)| 
        #     Q(ini__gt=data_ini, fim__lt=data_fim))
        prop = prop.exclude(id__in=reservas.values_list('propriedade', flat=True))

        return prop

class MinhasReservas(ListView):
    model = Reserva
    template_name = 'core/minhasreservas.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Minhas reservas'
        return context

    def get_queryset(self):
        return Reserva.objects.filter(hospede=self.request.user)

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

def reserva_detalhe_view(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)
    pode_editar = True
    if (reserva.dini < datetime.date.today() or reserva.dfim < datetime.date.today()):
        pode_editar = False
    return render(request, 'core/reserva.html', context={'reserva': reserva, 'user': request.user, 'editavel': pode_editar})

def add_propriedade_view(request): 
    form = PropriedadeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        propriedade = form.save(commit=False)
        propriedade.proprietario = request.user  # use your own profile here
        propriedade.save()
        return redirect('/accounts/propriedades/')
    return render(request, 'core/form_propriedade.html', {'form': form}) 

def apagar_propriedade_view(request, pk):
    propriedade = get_object_or_404(Propriedade, pk=pk)
    try:
        propriedade.delete()
        return redirect('/accounts/propriedades/')
    except ProtectedError as e:
        messages.error(request, 'Não foi possível remover a propriedade, pois ela já possui reservas.')
        return redirect('/propriedade/' + str(pk))

def edit_propriedade_view(request, pk): 
    instance = get_object_or_404(Propriedade, id=pk)
    form = PropriedadeEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/accounts/propriedades/')
    return render(request, 'core/form_edit_propriedade.html', {'form': form}) 

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

def edit_reserva_view(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)
    form = ReservaEditForm(request.POST or None, instance=reserva)
    form_pag = PagamentoEditForm(request.POST or None)
    if form.is_valid() and form_pag.is_valid():
        form.save()
        form_pag.save()
        return redirect('/reserva/' + str(pk))
    return render(request, 'core/form_edit_reserva.html', {'form': form, 'form_pag': form_pag}) 

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

def index_view(request):
    form = BuscaPropForm(request.POST or None)
    if (form.is_valid()):
        ini = form.cleaned_data['data_ini'].strftime('%Y-%m-%d')
        fim = form.cleaned_data['data_fim'].strftime('%Y-%m-%d')
        cidade = form.cleaned_data['cidade']
        return HttpResponseRedirect('/propriedades/'+ cidade +'/' + ini + '/' + fim)
    return render(request,'core/index.html', {'form': form})

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

def usuario_view(request):
    qtd_propriedades = Propriedade.objects.all().filter(proprietario=request.user).count()
    qtd_reservas = Reserva.objects.all().filter(hospede=request.user).count()

    usuario = request.user
    context = {'user': request.user, 'qtd': qtd_propriedades, 'qtdr': qtd_reservas}
    return render(request, 'core/user.html', context)

def edit_usuario_view(request):
    form = AtualizarUsuarioForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('/accounts/')
    return render(request, 'core/form_edit_user.html', {'form': form})