from django import forms
from .models import Categoria, Producto

class CategoriaForm(forms.ModelForm):
    estado = forms.BooleanField(
        required=False, 
        initial=True, 
        label="Activa (Marcar para Activar)",
    )

    class Meta:
        model = Categoria
        fields = ('nombre', 'estado') 
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Categoría'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'estado':
                 field.widget.attrs.update({'class': 'form-control'})
        if self.instance.pk:
            self.initial['estado'] = self.instance.estado == 1
            
    def clean_estado(self):
        return 1 if self.cleaned_data.get('estado') else 0

class ProductoForm(forms.ModelForm):
    estado = forms.BooleanField(
        required=False, 
        initial=True, 
        label="Disponible (Marcar para Activar)"
    )

    class Meta:
        model = Producto
        fields = ('id_categoria', 'nombre', 'descripcion', 'precio', 'stock', 'estado') 
        
        widgets = {
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción breve del producto'}),
            'precio': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'placeholder': '0'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['id_categoria'].queryset = Categoria.objects.filter(estado=1).order_by('nombre')
        for name, field in self.fields.items():
            if name != 'estado': 
                field.widget.attrs.update({'class': 'form-control'})
        if self.instance.pk:
            self.initial['estado'] = self.instance.estado == 1
            
    def clean_estado(self):
        return 1 if self.cleaned_data.get('estado') else 0