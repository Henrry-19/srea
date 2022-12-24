from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import *
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
class LoginFormView(LoginView):
    template_name='login.html'
    #success_url= reverse_lazy('login:index1') #Me redirecciona la URL y reverse_lazy->devuelve la ruta de la URL
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL) #Enviado esa dirección
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Iniciar sesión'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name='login' #El nombre del patrón de URL al que se redirigirá.
    
  
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

