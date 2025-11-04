from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        default='Sin Categoría',
        unique=True,
    )
    estado = models.IntegerField(
        default=1,
        verbose_name='Estado'
    )
    creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

class Producto(models.Model):
    id_categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.CASCADE,
        verbose_name='Categoría',
        db_column='id_categoria'
    )
    
    nombre = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name='Nombre del Producto'
    )
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción Detallada'
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Precio de Venta'
    )
    stock = models.IntegerField( 
        default=0, 
        verbose_name='Cantidad en Stock'
    )
    imagen = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
        verbose_name='URL/Ruta de Imagen'
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
        return self.nombre

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'