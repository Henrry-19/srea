from django.contrib import admin #Librería de adminitración
from django.urls import path, include #Librería permite incluir las urls
from django.conf import settings
from django.conf.urls.static import static
from apps.homepage.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),#Al inicio cargamos el administrador de Django
    path('accounts/', include('allauth.urls')),
    path('',include('apps.login.urls'),  name='login1'),
    path('srea/',include('apps.srea.urls', namespace='srea')),
    path('user/',include('apps.user.urls', namespace='user')),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #Configuracón para que se puedan leer los archivos
