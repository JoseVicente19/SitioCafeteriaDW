from django.urls import path
from .views import HomeView, login_view
from django.contrib.auth.views import LogoutView

app_name = 'home'
urlpatterns = [

    path('', HomeView.as_view(), name='homeapp'), 

    path('login/', login_view, name='login'), 

    path('logout/', LogoutView.as_view(), name='logout'),
]