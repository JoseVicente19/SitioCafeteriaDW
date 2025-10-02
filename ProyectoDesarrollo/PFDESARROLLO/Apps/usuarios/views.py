from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Role, Usuario, UsuarioRole
from .forms import UsuarioForm, RoleForm
from django import forms 


#VISTAS DE USUARIOS
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario_list.html'
    context_object_name = 'usuarios_list'

class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm 
    template_name = 'crearusuario.html' 
    success_url = reverse_lazy('usuarios:listausuarios') 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        form.fields['rol_seleccionado'] = forms.ModelChoiceField(
            queryset=Role.objects.all(),
            required=False,
            label='Asignar Rol Inicial',
            widget=forms.Select(attrs={'class': 'form-control'}) 
        )
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        
        usuario_creado = self.object
        rol_seleccionado = form.cleaned_data.get('rol_seleccionado')
        
        if rol_seleccionado:
            UsuarioRole.objects.create(
                id_usuario=usuario_creado,
                id_rol=rol_seleccionado
            )
        
        return response

class UsuarioUpdateView(UpdateView):

    model = Usuario
    form_class = UsuarioForm
    template_name = 'editarusuario.html'
    success_url = reverse_lazy('usuarios:listausuarios')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        rol_actual = UsuarioRole.objects.filter(id_usuario=self.object).first()
        initial_role = rol_actual.id_rol if rol_actual else None
        
        form.fields['rol_seleccionado'] = forms.ModelChoiceField(
            queryset=Role.objects.all(),
            required=False,
            label='Asignar Rol',
            initial=initial_role,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        return form

    def form_valid(self, form):
        usuario_original = self.get_object() 
        nueva_password = form.cleaned_data.get('password')

        if not nueva_password:
            form.cleaned_data['password'] = usuario_original.password
        
        response = super().form_valid(form)
        
        usuario_editado = self.object
        rol_seleccionado = form.cleaned_data.get('rol_seleccionado')
        
        UsuarioRole.objects.filter(id_usuario=usuario_editado).delete()
        
        if rol_seleccionado:
            UsuarioRole.objects.create(
                id_usuario=usuario_editado,
                id_rol=rol_seleccionado
            )
        
        return response


#VISTAS DE ROLES
class RoleListView(ListView):
    model = Role
    template_name = 'role_list.html' # Crearemos este template
    context_object_name = 'roles_list'

class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'crearform.html' # Usaremos el mismo form para crear y editar
    success_url = reverse_lazy('usuarios:listaroles') 


class RoleUpdateView(UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'editarform.html'
    success_url = reverse_lazy('usuarios:listaroles')
