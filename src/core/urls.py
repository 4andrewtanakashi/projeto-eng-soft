from django.urls import path
from .views import *

from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path('', index_view, name='index'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/propriedades/cadastrar/', login_required(add_propriedade_view), name='cadastrar'),
    path('accounts/propriedades/', login_required(MinhasPropriedades.as_view()), name='minhaspropriedades'),
    path('accounts/reservas/', login_required(MinhasReservas.as_view()), name='minhasreservas'),
    path('reserva/<uuid:pk>/', login_required(reserva_detalhe_view), name='reserva'),
    path('reserva/editar/<uuid:pk>/', login_required(edit_reserva_view), name='editreserva'),
    path('reserva/remover/<uuid:pk>/', login_required(apagar_reserva_view), name='removerreserva'),

    path('propriedades/<slug:cidade>/<slug:ini>/<slug:fim>', login_required(PropDisponiveis.as_view()), name='propriedades'),

    path('propriedade/<uuid:pk>/', login_required(prop_detalhe_view), name='propriedade'),
    path('propriedade/<uuid:pk>/<slug:ini>/<slug:fim>', login_required(prop_detalhe_reserva_view), name='propriedade'),
    path('propriedade/editar/<uuid:pk>/', login_required(edit_propriedade_view), name='editar'),
    path('propriedade/remover/<uuid:pk>/', login_required(apagar_propriedade_view), name='remover'),
    path('propriedade/reservar/<uuid:pk>/<slug:ini>/<slug:fim>', login_required(add_reserva_view), name='reservar'),

]