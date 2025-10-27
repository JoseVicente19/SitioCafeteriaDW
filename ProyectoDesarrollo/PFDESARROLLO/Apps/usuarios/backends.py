from .models import Usuario 
from django.contrib.auth.backends import BaseBackend

class UsuarioBackend(BaseBackend):

    def authenticate(self, request, nombre_u=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(nombre_u=nombre_u, estado=1) 
            
            if usuario.check_password(password):
                return usuario
            
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None