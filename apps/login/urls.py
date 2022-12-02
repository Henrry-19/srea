from django.contrib import admin
from django.urls import *
from apps.login.views import *

urlpatterns = [
    path('',LoginFormView.as_view(),  name='inicio_sesion'), #Permite ingresar al administrador
    path('logout/',LogoutRedirectView.as_view(), name='logout'), #Permite salir del administrador
]