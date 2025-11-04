

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from .forms import LoginForm 
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:homeapp') 
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre_u = form.cleaned_data['nombre_u']
            password = form.cleaned_data['password']
            

            user = authenticate(request, username=nombre_u, password=password) 
            
            if user is not None:

                if user.is_active:
                    login(request, user) 
                    messages.success(request, f'Bienvenido, {user.nombre_p or user.nombre_u}!') 
    
                    next_url = request.GET.get('next', 'home:homeapp') 
                    return redirect(next_url) 
                else:
                    messages.error(request, 'Su cuenta está inactiva.')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
        
    context = {'form': form}
    return render(request, 'login.html', context)