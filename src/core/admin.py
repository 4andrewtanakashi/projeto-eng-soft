from django.contrib import admin
from .models import Propriedade, Reserva, Pagamento

# Register your models here.
admin.site.register(Propriedade)
admin.site.register(Reserva)
admin.site.register(Pagamento)