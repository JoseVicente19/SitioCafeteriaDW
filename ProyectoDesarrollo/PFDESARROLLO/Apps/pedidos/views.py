from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView 
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Direccion, Pedido, ArticuloPedido
from django import forms
from .forms import DireccionForm, PedidoForm, ArticuloPedidoFormset 
from Apps.usuarios.models import Usuario
from Apps.productos.models import Producto
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from decimal import Decimal
from django.urls import reverse 

class DireccionListView(ListView):
    model = Direccion
    template_name = 'direccion_list.html'
    context_object_name = 'direcciones_list'

    def get_queryset(self):
        return Direccion.objects.filter(estado=1)

class DireccionCreateView(CreateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'creardireccion.html' 
    success_url = reverse_lazy('pedidos:listadirecciones') 

    def form_valid(self, form):
        
        form.instance.id_usuario = self.request.user 

        return super().form_valid(form)

class DireccionUpdateView(UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'actualizardireccion.html' 
    context_object_name = 'direccion' 
    success_url = reverse_lazy('pedidos:listadirecciones')

def dir_eliminar(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)
    direccion.estado = 0
    direccion.save()
    return redirect(reverse('pedidos:listadirecciones'))



class PedidoListView(ListView): 
    model = Pedido
    template_name = 'pedido_list.html' 
    context_object_name = 'pedidos'
    ordering = ['-fecha_pedido']

    def get_queryset(self):

        return super().get_queryset().filter(estado=1).exclude(estado_pedido='CARRITO').order_by('-fecha_pedido')


class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido_form.html' 
    success_url = reverse_lazy('pedidos:pedido_list') 
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['articulos_formset'] = ArticuloPedidoFormset(self.request.POST, self.request.FILES)
        else:
            data['articulos_formset'] = ArticuloPedidoFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        articulos_formset = context['articulos_formset']
        if self.request.user.is_authenticated and hasattr(self.request.user, 'usuario'):
            form.instance.id_usuario = self.request.user.usuario
        
        if not form.instance.estado_pedido:
            form.instance.estado_pedido = 'PENDIENTE'

        if articulos_formset.is_valid():
            with transaction.atomic():
                self.object = form.save() 
                
                articulos_formset.instance = self.object
                articulos_formset.save() 

                nuevo_total = 0
                for item in self.object.articulopedido_set.filter(estado=1):
                    nuevo_total += item.cantidad * item.precio_unitario
                
                self.object.total = nuevo_total
                self.object.save() 
                
            messages.success(self.request, '✅ Pedido registrado con éxito, incluyendo sus artículos.')
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, '❌ Hubo errores en el detalle de los artículos. Por favor, revise el formulario.')
            return self.render_to_response(self.get_context_data(form=form))


def obtener_precio_producto(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        producto_id = request.GET.get('producto_id')
        
        if producto_id:
            try:
                producto = get_object_or_404(Producto, id=producto_id)

                return JsonResponse({'precio': str(producto.precio)}) 
            except Exception:

                return JsonResponse({'precio': '0.00'})
        
        return JsonResponse({'precio': '0.00'})

    return JsonResponse({'error': 'Solicitud no válida'}, status=400)


class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'pedido_detail.html'
    context_object_name = 'pedido' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_actual = self.object        
        context['articulos_pedido'] = ArticuloPedido.objects.filter(id_pedido=pedido_actual)
        return context

class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido_update_form.html' 
    success_url = reverse_lazy('pedidos:pedido_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if not self.request.POST:
            data['articulos_formset'] = ArticuloPedidoFormset(instance=self.object)

        return data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        form = self.get_form()
        articulos_formset = ArticuloPedidoFormset(request.POST, instance=self.object)
        
        self.articulos_formset = articulos_formset 
        
        if form.is_valid() and articulos_formset.is_valid():
            return self.form_valid(form, articulos_formset)
        else:
            return self.form_invalid(form, articulos_formset)

    def form_valid(self, form, articulos_formset):
        total_calculado = Decimal('0.00')

        for articulo_data in articulos_formset.cleaned_data:
            if articulo_data and not articulo_data.get('DELETE', False):
                cantidad = articulo_data.get('cantidad') or 0
                precio = articulo_data.get('precio_unitario') or 0
                
                if isinstance(cantidad, int) and isinstance(precio, Decimal):
                    total_calculado += cantidad * precio
                
        form.instance.total = total_calculado 
        
        try:
            with transaction.atomic():
                self.object = form.save()
                
                articulos_formset.instance = self.object
                articulos_formset.save()
            
            messages.success(self.request, f"✅ El Pedido #{self.object.pk} ha sido actualizado correctamente.")
            return redirect(self.get_success_url())
            
        except Exception as e:
            messages.error(self.request, f"❌ Hubo un error al guardar el pedido: {e}")
            return self.form_invalid(form, articulos_formset)

    def form_invalid(self, form, articulos_formset):
        context = self.get_context_data(form=form, articulos_formset=articulos_formset)
        return self.render_to_response(context)

def pedido_eliminar(request, pk):

    pedido = get_object_or_404(Pedido, pk=pk)
    
    pedido.estado = 0
    pedido.save()

    return redirect(reverse('pedidos:pedido_list')) 
