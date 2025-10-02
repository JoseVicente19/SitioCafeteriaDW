"""
URL configuration for ColegioA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import UsuarioListView , UsuarioCreateView, UsuarioUpdateView
from .views import RoleListView , RoleCreateView, RoleUpdateView

app_name='usuarios'
urlpatterns = [
    path('', UsuarioListView.as_view(), name='listausuarios'),
    path('crear/', UsuarioCreateView.as_view(), name='crearusuario'),
    path('editar/ <int:pk>', UsuarioUpdateView.as_view(), name='editarusuario'),

    #PATHS PARA ROLES
    path('roles/', RoleListView.as_view(), name='listaroles'),
    path('roles/crear/', RoleCreateView.as_view(), name='crearrol'),
    path('roles/editar/<int:pk>/', RoleUpdateView.as_view(), name='editarrol'),

]
