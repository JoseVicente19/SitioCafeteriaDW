from django import forms
from .models import Usuario, Role

class UsuarioForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar Contraseña"
    )
    
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
            self.fields['password_confirm'].required = False 

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        if self.instance.pk and not password:
            if 'password' in self.cleaned_data: del self.cleaned_data['password']
            if 'password_confirm' in self.cleaned_data: del self.cleaned_data['password_confirm']
        
        return self.cleaned_data

    # HASHEO AUTOMÁTICO cuando se gfuarda
    def save(self, commit=True):

        user = super().save(commit=False)
    
        if self.cleaned_data.get("password"):

            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            
        return user

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__' 

        widgets = {
             'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
             'nombre': forms.TextInput(attrs={'class': 'form-control'}),
         }