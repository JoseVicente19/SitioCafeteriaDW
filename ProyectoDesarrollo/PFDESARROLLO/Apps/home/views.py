from django.shortcuts import render
from django.views.generic import TemplateView

# Crea tus vistas aquí.

class HomeView(TemplateView):
    template_name = 'home.html'