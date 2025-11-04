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

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_u, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El Usuario debe tener un correo electrónico')
        if not nombre_u:
            raise ValueError('El Usuario debe tener un nombre de usuario')
            
        correo = self.normalize_email(correo)
        usuario = self.model(nombre_u=nombre_u, correo=correo, **extra_fields)
        
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre_u, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('estado', 1) 
        
        return self.create_user(nombre_u, correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin): 
    
    USERNAME_FIELD = 'nombre_u' 
    REQUIRED_FIELDS = ['correo'] 
    
    nombre_u = models.CharField(max_length=100, unique=True, verbose_name='Nombre de Usuario')
    correo = models.EmailField(max_length=100, unique=True, verbose_name='Correo Electrónico')
    password = models.CharField(max_length=255, verbose_name='Contraseña') 
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    estado = models.IntegerField(default=1, verbose_name='Estado')
    nombre_p = models.CharField(max_length=75, null=True, blank=True, verbose_name='Nombre Personal')
    telefono = models.CharField(max_length=75, null=True, blank=True, verbose_name='Teléfono')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    
    objects = UsuarioManager() 
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_full_name(self):
        return self.nombre_p or self.nombre_u

    def get_short_name(self):
        return self.nombre_u

    # MÉTODOS DE ROL PARA CONTROL DE ACCESO
    def is_admin(self):
        return self.usuariosrole_set.filter(id_rol__descripcion='Administrador', id_rol__estado=1).exists()

    def is_staff_operaciones(self):
        return self.usuariosrole_set.filter(id_rol__descripcion='Empleado', id_rol__estado=1).exists()

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