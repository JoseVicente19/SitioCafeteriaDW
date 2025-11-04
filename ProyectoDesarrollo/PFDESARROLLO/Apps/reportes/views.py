from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Reporte
from django.views.generic import TemplateView
from datetime import date
from django.contrib import messages
from django.shortcuts import redirect
from Apps.pedidos.models import Pedido, ArticuloPedido
from django.contrib.auth.decorators import login_required
# Create your views here.

class DashboardReportesView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ultimo_reporte = Reporte.objects.filter(estado=1).order_by('-fecha_reporte').first()

        context['ventas_dia'] = "N/D"
        context['pedidos_dia'] = "N/D"
        context['productos_tabla'] = []
        
        if ultimo_reporte:
            context['ventas_dia'] = ultimo_reporte.total_ventas_dia
            context['pedidos_dia'] = ultimo_reporte.numero_pedidos_dia
            context['fecha_reporte'] = ultimo_reporte.fecha_reporte
    
            try:
                productos_json = json.loads(ultimo_reporte.productos_mas_vendidos or '{}')
                principal = productos_json.get('producto_principal')
                if principal:
                    context['productos_tabla'] = [{
                        'nombre': principal.get('nombre', 'N/D'),
                        'cantidad': principal.get('ventas', 0),
                        'total': ultimo_reporte.total_ventas_dia 
                    }]
            except Exception:
                context['productos_tabla'] = []
                
        return context

@login_required 
def generar_reporte_dia(request):
    
    if request.method != 'POST':
        messages.error(request, "Acceso no permitido.")
        return redirect('reportes:dashboard')
    
    # 1. Importaciones Corregidas
    hoy = date.today()
    
    # 2. Verificar si el reporte ya existe
    if Reporte.objects.filter(fecha_reporte=hoy).exists():
        messages.warning(request, f"El reporte para el día {hoy} ya existe.")
        return redirect('reportes:dashboard')

    try:

        pedidos_hoy = Pedido.objects.filter(
            fecha__date=hoy, 
            estado='Completado'
        )
        
        # A. Total de Ventas y Número de Pedidos
        resultados_totales = pedidos_hoy.aggregate(
            total_ventas=Sum('total_final'),
            num_pedidos=Count('id')
        )
        
        total_ventas = resultados_totales['total_ventas'] or 0.00
        num_pedidos = resultados_totales['num_pedidos'] or 0
        
        productos_vendidos = ArticuloPedido.objects.filter(
            pedido__in=pedidos_hoy 
        ).values('producto__id', 'producto__nombre').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')
        
        productos_json_data = {"otros_productos": [], "producto_principal": None}
        
        if productos_vendidos:
            top_producto = productos_vendidos.first()
            productos_json_data["producto_principal"] = {
                "id": top_producto['producto__id'],
                "nombre": top_producto['producto__nombre'],
                "ventas": float(top_producto['total_vendido'])
            }
            
        Reporte.objects.create(
            fecha_reporte=hoy,
            total_ventas_dia=total_ventas,
            numero_pedidos_dia=num_pedidos,
            productos_mas_vendidos=json.dumps(productos_json_data)
        )
        
        messages.success(request, f"Reporte automático generado exitosamente para {hoy}.")
        
    except AttributeError as e:

        messages.error(request, f"Error de atributo en los modelos (ej. campo faltante): {e}")
    except Exception as e:
        messages.error(request, f"Error general al generar el reporte: {e}")

    return redirect('reportes:dashboard')