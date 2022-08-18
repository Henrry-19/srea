from tkinter.font import names
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from apps.login.views import LoginFormView
from apps.homepage.views import IndexView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('apps.login.urls'),  name='login1'),
    path('srea/',include('apps.srea.urls', namespace='srea')),
    path('',IndexView.as_view(), name="index"),
    #path('accounts/', include('allauth.urls')),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
