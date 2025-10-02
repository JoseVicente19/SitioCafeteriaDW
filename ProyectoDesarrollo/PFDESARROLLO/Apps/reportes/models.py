from django.db import models

# Create your models here.

class Reporte(models.Model):
    fecha_reporte = models.DateField(
        verbose_name='Fecha del Reporte'
    )
    
    total_ventas_dia = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Total de Ventas del Día'
    )
    
    numero_pedidos_dia = models.IntegerField(
        verbose_name='Número de Pedidos del Día'
    )
    
    productos_mas_vendidos = models.TextField( 
        null=True,
        blank=True,
        verbose_name='JSON de Productos más Vendidos'
    )
    
    creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )
    
    estado = models.IntegerField(
        default=1,
        verbose_name='Estado'
    )

    def __str__(self):
        return f"Reporte de {self.fecha_reporte}"

    class Meta:
        db_table = 'reporte'
        verbose_name = 'Reporte de Ventas'
        verbose_name_plural = 'Reportes de Ventas'