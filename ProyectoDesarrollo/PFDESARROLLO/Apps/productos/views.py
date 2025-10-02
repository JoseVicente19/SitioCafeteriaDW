from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from django import forms


PRODUCTO_SUCCESS_URL = reverse_lazy('productos:listaproductos') 
SUCCESS_URL = reverse_lazy('productos:listacategoria') 


class ProductoListView(ListView):
    model = Producto
    template_name = 'productolist.html' 
    context_object_name = 'productos'
    paginate_by = 10
    queryset = Producto.objects.select_related('id_categoria').all().order_by('nombre')


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'crearproducto.html' 
    success_url = PRODUCTO_SUCCESS_URL


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'editarproducto.html' 
    success_url = PRODUCTO_SUCCESS_URL 


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html' 
    context_object_name = 'categorias' 
    paginate_by = 10  
    queryset = Categoria.objects.all().order_by('nombre') 

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'crearcat.html' 
    success_url = SUCCESS_URL 


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'editarcat.html' 
    success_url = SUCCESS_URL 