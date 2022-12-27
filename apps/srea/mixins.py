from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from crum import get_current_request  #Permite obtener la sesión actual del usuario

class IsSuperuserMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['date_now'] = datetime.now()
        return context

class ValidatePermissionRequiredMixin(object):
    permission_required= ''
    url_redirect = None

    def get_perms(self):
        perms=[]
        if isinstance(self.permission_required,str):
            perms.append(self.permission_required)
        else:
            perms=list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('srea:index1')
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            
        if 'group' in request.session: 
            group=request.session['group']
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para acceder a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para acceder a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())



    