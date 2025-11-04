from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Reporte
from django.views.generic import TemplateView
from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from Apps.pedidos.models import Pedido, ArticuloPedido
from Apps.productos.models import Producto
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


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
def generar_reporte(request):
    if request.method == "POST":
        date_hoy = date.today()
        pedidos_dia = Pedido.objects.filter(fecha_pedido__date=date_hoy)
        if not pedidos_dia.exists():
            messages.warning(request, "No hay pedidos para generar el reporte de hoy.")
            return redirect('reportes:dashboard')

        total_ventas = pedidos_dia.aggregate(total=Sum('total'))['total'] or 0
        num_pedidos = pedidos_dia.count()

        articulos_dia = ArticuloPedido.objects.filter(id_pedido__fecha_pedido__date=date_hoy)
        producto_top = (
            articulos_dia.values('id_producto')
            .annotate(total_vendido=Sum('cantidad'))
            .order_by('-total_vendido')
            .first()
        )

        productos_json = {}
        if producto_top:
            producto = Producto.objects.filter(id=producto_top['id_producto']).first()
            nombre_producto = producto.nombre if producto else "Desconocido"
            productos_json = {
                "producto_principal": {
                    "nombre": nombre_producto,
                    "ventas": producto_top["total_vendido"]
                }
            }

        Reporte.objects.update_or_create(
            fecha_reporte=date_hoy,
            defaults={
                "total_ventas_dia": total_ventas,
                "numero_pedidos_dia": num_pedidos,
                "productos_mas_vendidos": json.dumps(productos_json, cls=DjangoJSONEncoder),
                "estado": 1
            }
        )

        messages.success(request, f"✅ Reporte generado o actualizado correctamente para {date_hoy}.")
        return HttpResponseRedirect(reverse('reportes:dashboard'))

    return redirect('reportes:dashboard')
