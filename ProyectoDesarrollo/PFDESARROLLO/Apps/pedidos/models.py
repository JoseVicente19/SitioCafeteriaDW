from django.db import models
from Apps.usuarios.models import Usuario
from Apps.productos.models import Producto


# Create your models here.

class Direccion(models.Model):
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name='Usuario Propietario',
        db_column='id_usuario'
    )
    
    calle = models.CharField(
        max_length=255, 
        verbose_name='Calle'
    )
    numero = models.CharField( 
        max_length=20,
        verbose_name='Número Exterior/Interior De Casa'
    )
    municipio = models.CharField( 
        max_length=100,
        verbose_name='Municipio/Localidad'
    )
    departamento = models.CharField( 
        max_length=100,
        verbose_name='Departamento/Estado'
    )
    codigo_postal = models.CharField( 
        max_length=20,
        null=True, 
        blank=True,
        verbose_name='Código Postal'
    )
    referencia = models.TextField( 
        null=True,
        blank=True,
        verbose_name='Referencia Adicional'
    )
    
    estado = models.IntegerField(
        default=1,
        verbose_name='Estado'
    )
    creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )

    def __str__(self):
        return f"{self.calle} #{self.numero}, {self.municipio}, {self.departamento}"

    class Meta:
        db_table = 'direccion'
        verbose_name = 'Dirección de Usuario'
        verbose_name_plural = 'Direcciones de Usuarios'


class Pedido(models.Model):
    ESTADO_OPCIONES = (
        ('PENDIENTE', 'Pendiente de Pago'),
        ('PROCESO', 'En Proceso'),
        ('ENVIADO', 'Enviado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    )

    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name='Usuario que realiza el pedido',
        db_column='id_usuario'
    )
    
    id_direccion = models.ForeignKey(
        'Direccion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Dirección de Entrega',
        db_column='id_direccion'
    )
    
    fecha_pedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y Hora de Pedido'
    )
    
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00, 
        verbose_name='Monto Total del Pedido'
    )
    
    estado_pedido = models.CharField(
        max_length=50,
        choices=ESTADO_OPCIONES, 
        default='CARRITO', 
        verbose_name='Estado del Pedido'
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
        return f"Pedido #{self.id} de {self.id_usuario.nombre_u} - Estado: {self.get_estado_pedido_display()}"

    def recalcular_total(self):

        total_articulos = self.articulopedido_set.aggregate(
            subtotal=Sum(F('cantidad') * F('precio_unitario'), output_field=models.DecimalField())
        )['subtotal'] or 0.00
        
        self.total = total_articulos
        self.save()

    class Meta:
        db_table = 'pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']


class ArticuloPedido(models.Model):
    id_pedido = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        verbose_name='Pedido Asociado',
        db_column='id_pedido'
    )
    
    id_producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,
        verbose_name='Producto Comprado',
        db_column='id_producto'
    )
    
    cantidad = models.IntegerField(
        verbose_name='Cantidad Comprada'
    )
    
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio de Venta'
    )

    creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    estado = models.IntegerField(
        default=1,
        verbose_name='Estado'
    )


    def get_subtotal(self):
        return self.cantidad * self.precio_unitario
        
    def __str__(self):
        return f"{self.cantidad} de {self.id_producto.nombre} en Pedido #{self.id_pedido.id}"

    class Meta:
        db_table = 'articulopedido'
        verbose_name = 'Artículo de Pedido'
        verbose_name_plural = 'Artículos de Pedidos'
        unique_together = (('id_pedido', 'id_producto'),)