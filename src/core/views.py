from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

from django.db.models import Q

from django.views.generic import ListView, FormView
from .models import Propriedade, Reserva, Pagamento
from .forms import PropriedadeForm, ReservaForm, PagamentoForm, BuscaPropForm # RegistrarForm
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
import datetime
import time


# Create your views here.

class BuscaProp(ListView):
    model = Propriedade
    template_name = 'core/propriedades.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Propriedades do sistema"
        return context

class MinhasPropriedades(ListView):
    model = Propriedade
    template_name = 'core/propriedades.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Minhas propriedades"
        return context

    def get_queryset(self):
        return Propriedade.objects.filter(proprietario=self.request.user)

class PropDisponiveis(ListView):
    model = Propriedade
    template_name = 'core/propriedades.html'

    def get_queryset(self):
        data_ini = datetime.datetime.strptime(self.kwargs['ini'],'%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(self.kwargs['fim'],'%Y-%m-%d').date()

        prop = Propriedade.objects.filter(cidade__icontains=self.kwargs['cidade'])


        reservas = Reserva.objects.filter(propriedade__in=prop).filter(
            Q(ini__lte=data_fim, fim__gte=data_ini)
        )

        # reservas = Reserva.objects.filter(propriedade__in=prop).filter(
        #     Q(ini__lte=data_ini, fim__gte=data_fim) | # ok
        #     Q(ini__gt=data_ini, fim__gt=data_fim, fim__gt=data_ini)| 
        #     Q(ini__lt=data_ini, fim__lt=data_fim, fim__gt=data_ini)| 
        #     Q(ini__gt=data_ini, fim__lt=data_fim))
        prop = prop.exclude(id__in=reservas.values_list('propriedade', flat=True))

        return prop

def prop_detalhe_view(request, pk):
    propriedade = get_object_or_404(Propriedade, id=pk)
    return render(request, 'core/propriedade.html', context={'prop': propriedade, 'user': request.user})

def add_propriedade_form(request): 
    form = PropriedadeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        propriedade = form.save(commit=False)
        propriedade.proprietario = request.user  # use your own profile here
        propriedade.save()
        return redirect('/minhasprop/')
    return render(request, 'core/form_propriedade.html', {'form': form}) 

def edit_propriedade_form(request, pk): 
    instance = get_object_or_404(Propriedade, id=pk)
    form = PropriedadeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/minhasprop/')
    return render(request, 'core/form_propriedade.html', {'form': form}) 

def add_reserva(request, pk):
    form = ReservaForm(request.POST or None)
    formPagamento = PagamentoForm(request.POST or None)
    if form.is_valid() and formPagamento.is_valid():
        reserva = form.save(commit=False)
        reserva.hospede = request.user
        reserva.propriedade = get_object_or_404(Propriedade, id=pk)
        reserva.propriedade.status = 'i'
        reserva.propriedade.save()
        pagamento = formPagamento.save()
        reserva.dados_pagamento = pagamento
        reserva.save()
        return redirect('/propriedades/')
    return render(request, 'core/form_reserva.html', {'form': form, 'form_pag': formPagamento}) 


def index(request):
    return render(
        request,
        'core/index.html'
    )

def signup(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'core/signup.html', context)

def busca_cidade(request):
    form = BuscaPropForm(request.POST or None)
    if (form.is_valid()):
        ini = form.cleaned_data['data_ini'].strftime('%Y-%m-%d')
        fim = form.cleaned_data['data_fim'].strftime('%Y-%m-%d')
        cidade = form.cleaned_data['cidade']
        return HttpResponseRedirect('/propriedades/'+ cidade +'/' + ini + '/' + fim)
    return render(request, 'core/busca.html', {'form': form})