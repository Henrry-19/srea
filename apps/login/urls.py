from tkinter.font import names
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from apps.login.views import *
urlpatterns = [
    path('',LoginFormView.as_view(),  name='login'),
    #path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/',LogoutRedirectView.as_view(), name='logout'),
]
