from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import functions

# Create your models here.

class Role(models.Model):
    descripcion = models.CharField(
        max_length=50,
        verbose_name='Nombre del Rol'
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
        return self.descripcion

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'

class Usuario(models.Model):   
    nombre_u = models.CharField(max_length=100, unique=True, verbose_name='Nombre de Usuario')
    correo = models.EmailField(max_length=100, unique=True, verbose_name='Correo Electrónico')
    password = models.CharField(max_length=255, verbose_name='Contraseña') 
    estado = models.IntegerField(default=1, verbose_name='Estado')
    nombre_p = models.CharField(max_length=75, null=True, blank=True, verbose_name='Nombre Personal')
    telefono = models.CharField(max_length=75, null=True, blank=True, verbose_name='Teléfono')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    
    def __str__(self):
        return self.correo

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario del Sistema'
        verbose_name_plural = 'Usuarios del Sistema'

class UsuarioRole(models.Model):
    id_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        verbose_name='Usuario',
        db_column='id_usuario'
    )

    id_rol = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        verbose_name='Rol',
        db_column='id_rol'
    )

    creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Asignación'
    )

    def __str__(self):
        return f"{self.id_usuario.nombre_u} - {self.id_rol.descripcion}"

    class Meta:
        db_table = 'usuariosroles'
        verbose_name = 'Asignación de Rol'
        verbose_name_plural = 'Asignaciones de Roles'
        unique_together = (('id_usuario', 'id_rol'),)