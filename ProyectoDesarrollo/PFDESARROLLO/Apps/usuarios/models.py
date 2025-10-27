from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import functions
from django.contrib.auth.hashers import make_password, check_password
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
    USERNAME_FIELD = 'nombre_u'
    REQUIRED_FIELDS = ['correo'] 
    
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

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_active(self):
        return self.estado == 1
    
    def is_staff(self):
        return False

    def has_perm(self, perm, obj=None):
        return self.is_staff()


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