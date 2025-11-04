from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Role, Usuario, UsuarioRole
from .forms import UsuarioForm, RoleForm
from django import forms 
from django.contrib.auth.hashers import make_password


#VISTAS DE USUARIOS
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario_list.html'
    context_object_name = 'usuarios_list'   
    def get_queryset(self):
        return Usuario.objects.filter(estado=1).order_by('nombre_p')

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
        self.object = form.save() 
        
        usuario_creado = self.object
        rol_seleccionado = form.cleaned_data.get('rol_seleccionado')
        
        if rol_seleccionado:
            UsuarioRole.objects.create(
                id_usuario=usuario_creado,
                id_rol=rol_seleccionado
            )
        
        return super().form_valid(form)

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

def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    usuario.estado = 0
    usuario.save()
    return redirect('usuarios:listausuarios')

class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'usuario_detail.html'
    context_object_name = 'usuario' 


#VISTAS DE ROLES
class RoleListView(ListView):
    model = Role
    template_name = 'role_list.html' 
    context_object_name = 'roles_list'
    
    def get_queryset(self):
        return Role.objects.filter(estado=1).order_by('descripcion') 

class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'crearform.html' 
    success_url = reverse_lazy('usuarios:listaroles') 

class RoleUpdateView(UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'editarform.html'
    success_url = reverse_lazy('usuarios:listaroles')

def rol_eliminar(request, pk):
    rol = get_object_or_404(Role, pk=pk)
    rol.estado = 0
    rol.save()
    return redirect('usuarios:listaroles') 