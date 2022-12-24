from django.contrib import admin
from django.urls import *
from apps.login.views import *
from apps.homepage.views import IndexView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',LoginFormView.as_view(),  name='login'), #Permite ingresar al administrador
    path('logout/',LogoutRedirectView.as_view(), name='logout'), #Permite salir del administrador
]
