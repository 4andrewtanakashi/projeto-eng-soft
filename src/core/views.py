from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, FormView
from .models import Propriedade, Reserva, Pagamento
from .forms import PropriedadeForm, ReservaForm # RegistrarForm
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404


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
    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.hospede = request.user
        reserva.propriedade = get_object_or_404(Propriedade, id=pk)
        reserva.propriedade.status = 'i'
        reserva.propriedade.save()
        pagamento = Pagamento()
        pagamento.save()
        reserva.dados_pagamento = pagamento
        reserva.save()
        return redirect('/propriedades/')
    return render(request, 'core/form_reserva.html', {'form': form}) 


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

