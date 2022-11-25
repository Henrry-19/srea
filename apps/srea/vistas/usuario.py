from pickle import FALSE
from re import template
import re
from urllib import request
from django.contrib.auth.decorators import login_required #Importación de decoradores
from django.utils.decorators import method_decorator #Importación del método decorador
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import *
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


from apps.srea.forms import *
from apps.srea.models import Usuario

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


class ListadoUsuario(ListView):
    model = Usuario
    template_name = 'usuarios/usuario_lista.html'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo = True)

class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = UsuarioCreateForm
    template_name = 'usuarios/usuario_create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) #Obteniendo toda la información que me están enviando de la petición
        if form.is_valid():
            nuevo_usuario = Usuario(
                email = form.cleaned_data.get('email'),
                username = form.cleaned_data.get('username'),
                nombres = form.cleaned_data.get('nombres'),
                apellidos = form.cleaned_data.get('apellidos')
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            return redirect('srea:principal')
        else:
            return render(request,self.template_name,{'form':form})


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuario/usuario_delete.html'
    success_url=reverse_lazy('srea:principal')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Usuario'
        context['modelo'] = 'Usuario'
        context['url_lista'] = reverse_lazy('srea:principal')
        return context

class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioCreateForm
    template_name = 'usuario/usuario_create.html'
    success_url = reverse_lazy('srea:usuario')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}                                     
        try:
            action= request.POST['action']
            if action =='edit':
                form = self.get_form() ###
                data=form.save()
            else:
                data['error']='No realiza ninguna acción'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualización de un usuario'
        context['entity'] = 'Usuario'
        context['url_lista'] = reverse_lazy('srea:principal')
        context['action'] = 'edit'
        return context

class Usuario1UpdateView(UpdateView):
    model=Usuario
    fields=['email','username','nombres', 'apellidos']
    template_name='usuarios/usuario_create.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:principal')

