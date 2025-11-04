from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

class AdminRequiredMixin(AccessMixin):
    permission_denied_message = "No tienes permiso para acceder a esta página."
    login_url = '/' 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def admin_required(function=None, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_admin(), 
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator