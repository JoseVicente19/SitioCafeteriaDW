from django import forms
from .models import Direccion, Pedido, ArticuloPedido
from Apps.usuarios.models import Usuario

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion

        fields = [
            'calle', 
            'numero', 
            'municipio', 
            'departamento', 
            'codigo_postal', 
            'referencia'
        ]

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['id_usuario', 'id_direccion', 'estado_pedido', 'estado']


from django.forms.models import inlineformset_factory


ArticuloPedidoFormset = inlineformset_factory(
    Pedido,             
    ArticuloPedido,    
    fields=['id_producto', 'cantidad', 'precio_unitario'],
    extra=0,
    can_delete=True
)