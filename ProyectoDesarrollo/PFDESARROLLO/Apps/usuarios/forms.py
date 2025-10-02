from django import forms
from .models import Usuario, Role

class UsuarioForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = [
            'nombre_u', 
            'correo', 
            'password', 
            'estado', 
            'nombre_p', 
            'telefono'
        ] 
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['password'].required = False


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__' 

        widgets = {
             'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
             'nombre': forms.TextInput(attrs={'class': 'form-control'}),
         }