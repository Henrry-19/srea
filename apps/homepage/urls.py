from django.contrib import admin
from django.urls import path
from apps.homepage.views  import Index1View, Index2View

app_name="apps.homepage" 

urlpatterns = [
    path('index1/',(Index1View.as_view()), name="index1"),#Presenta primera vista de Inicio (homepage-index)
    path('index2/',(Index2View.as_view()), name="index2"),#Presenta segunda vista de Inicio (vtc-encabezado)
]
