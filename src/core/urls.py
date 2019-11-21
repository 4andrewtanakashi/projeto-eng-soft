from django.urls import path
from .views import *

from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path("", index, name="index"),
    path("accounts/signup/", signup, name="signup"),
    path('propriedades/', login_required(BuscaProp.as_view()), name='todas'),
    path('propriedade/<uuid:pk>', login_required(prop_detalhe_view), name='propriedade'),
    path('cadastrar/', login_required(add_propriedade_form), name='cadastrar'),
    path('minhasprop/', login_required(MinhasPropriedades.as_view()), name='minhaspropriedades'),
    path('editar/<uuid:pk>', login_required(edit_propriedade_form), name='editar'),
    path('reservar/<uuid:pk>', login_required(add_reserva), name='reservar'),
]