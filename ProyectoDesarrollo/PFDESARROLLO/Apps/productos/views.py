from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
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
    queryset = Producto.objects.select_related('id_categoria').filter(estado=1).order_by('nombre')


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

def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.estado = 0
    producto.save()
    return redirect('productos:listaproductos')

class ProductoDetailView(DetailView):
    model = Producto

    template_name = 'producto_detail.html' 
    context_object_name = 'producto' 


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html' 
    context_object_name = 'categorias' 
    paginate_by = 10  
    queryset = Categoria.objects.filter(estado=1).order_by('nombre')

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

def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)  
    Producto.objects.filter(id_categoria=categoria).update(estado=0) #
    categoria.estado = 0
    categoria.save()
    return redirect('productos:listacategoria') 