from django.urls import path
from .views import *

from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path("", index, name="index"),
    path("accounts/signup/", signup_view, name="signup"),
    path('propriedades/', login_required(BuscaProp.as_view()), name='todas'),

    path('accounts/propriedades/cadastrar/', login_required(add_propriedade_view), name='cadastrar'),
    path('accounts/propriedades/', login_required(MinhasPropriedades.as_view()), name='minhaspropriedades'),
    path('propriedades/<slug:cidade>/<slug:ini>/<slug:fim>', login_required(PropDisponiveis.as_view()), name='propriedades'),
    path('busca', login_required(busca_cidade), name='buscar'),

    path('propriedade/<uuid:pk>/', login_required(prop_detalhe_view), name='propriedade'),
    path('propriedade/editar/<uuid:pk>/', login_required(edit_propriedade_view), name='editar'),
    path('propriedade/remover/<uuid:pk>/', login_required(apagar_propriedade_view), name='remover'),
    path('propriedade/reservar/<uuid:pk>/<slug:ini>/<slug:fim>', login_required(add_reserva), name='reservar'),


]