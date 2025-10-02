from django.contrib import admin
from .models import Direccion, Pedido, ArticuloPedido

# Register your models here.


admin.site.register(Direccion)
admin.site.register(Pedido)
admin.site.register(ArticuloPedido)


