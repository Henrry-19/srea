from django.contrib import admin #Librería de adminitración
from django.urls import path, include #Librería permite incluir las urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),#Al inicio cargamos el administrador de Django
    path('',include('apps.login.urls'),  name='login1'),
    path('home/',include('apps.homepage.urls',namespace='home')),
    path('srea/',include('apps.srea.urls', namespace='srea')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #Configuracón para que se puedan leer los archivos
