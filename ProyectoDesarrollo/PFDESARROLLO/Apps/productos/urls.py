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
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, producto_eliminar, ProductoDetailView
from .views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, categoria_eliminar

app_name='productos'
urlpatterns = [
#URLS PRODUCTOS
    path('', ProductoListView.as_view(), name='listaproductos'),
    path('crear', ProductoCreateView.as_view(), name='crearproductos'),
    path('editar/<int:pk>', ProductoUpdateView.as_view(), name='editarproducto'),
    path('<int:pk>/eliminar/', producto_eliminar, name='producto_eliminar'),
    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),

    #URLS PARA CATEGORIA
    path('categoria/', CategoriaListView.as_view(), name='listacategoria'),
    path('categoria/crear/', CategoriaCreateView.as_view(), name='crearcategoria'),
    path('categoria/editar/ <int:pk>', CategoriaUpdateView.as_view(), name='editarcategoria'),
    path('categoria/<int:pk>/eliminar/', categoria_eliminar, name='categoria_eliminar'),
]
