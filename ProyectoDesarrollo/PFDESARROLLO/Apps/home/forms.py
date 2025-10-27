from django import forms

class LoginForm(forms.Form):
    nombre_u = forms.CharField(
        max_length=100, 
        label='Nombre de Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )