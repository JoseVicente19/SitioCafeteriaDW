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
from .views import DireccionListView, DireccionCreateView, DireccionUpdateView, dir_eliminar
from .views import PedidoListView, PedidoCreateView, obtener_precio_producto, PedidoDetailView, PedidoUpdateView, pedido_eliminar


app_name='pedidos'
urlpatterns = [


#URLS DIRECCION
    path('direcciones/', DireccionListView.as_view(), name='listadirecciones'),
    path('direcciones/crear/', DireccionCreateView.as_view(), name='creardirecciones'),
    path('direcciones/editar/<int:pk>/', DireccionUpdateView.as_view(), name='editardirecciones'), 
     path('direcciones/<int:pk>/eliminar/', dir_eliminar, name='dir_eliminar'),
    

#URLS DE PEDIDO
    path('', PedidoListView.as_view(), name='pedido_list'),
    path('crear/', PedidoCreateView.as_view(), name='crearpedido'),
    path('ajax/obtener_precio/', obtener_precio_producto, name='obtener_precio_producto'),
    path('<int:pk>/', PedidoDetailView.as_view(), name='pedido_detail'),
    path('<int:pk>/editar/', PedidoUpdateView.as_view(), name='pedido_update'),
    path('<int:pk>/eliminar/', pedido_eliminar, name='pedido_eliminar'), 

]