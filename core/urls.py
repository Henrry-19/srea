from tkinter.font import names
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from apps.login.views import LoginFormView
from apps.homepage.views import IndexView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('apps.login.urls'),  name='login1'),
    path('srea/',include('apps.srea.urls', namespace='srea')),
    path('',IndexView.as_view(), name="index"),
    #path('accounts/', include('allauth.urls')),

]
