from django.contrib import admin
from .models import Propriedade, Reserva, Pagamento

# Permitir o cadastro dos modelos no painel do administrador
admin.site.register(Propriedade)
admin.site.register(Reserva)
admin.site.register(Pagamento)