from django.contrib import admin
from django.urls import *
from apps.login.views import *


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',LoginFormView.as_view(),  name='login'), #Permite ingresar al administrador
    path('logout/',LogoutRedirectView.as_view(), name='logout'), #Permite salir del administrador
    path('reset/password',ResetPasswordView.as_view(), name='reset_password'), #Permite resetear la clave
    path('change/password/<str:token>/',ChangePasswordView.as_view(), name='change_password'), #Permite crear el formulario para cambiar la clave
]
