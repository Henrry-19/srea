from tkinter.font import names
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomeView.as_view(),  name='home'),
    path('srea/',include('srea.urls', namespace='srea')),
    path('accounts/', include('allauth.urls')),

]
