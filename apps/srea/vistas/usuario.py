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

class UsuarioListView(ListView): 
    model = Usuario
    template_name = 'usuario/usuario_lista.html'
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Usuario.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de usuarios'
        context['url_create'] = reverse_lazy('srea:usuario')
        context['url_lista'] = reverse_lazy('srea:principal')
        context['modelo'] = 'Usuarios'
        return context

class UsuarioCreateView(View):
    model: Usuario  #Indicar el modelo con el cual se va ha trabajar
    form= UsuarioCreateForm() # Indicar el formulario con el que se va ha trabajar
    template_name='./usuario/usuario_create.html' #Indicar cual es el template para crear el registro 
    success_url= reverse_lazy('srea:principal') #Me redirecciona la URL y reverse_lazy->devuelve la ruta de la URL
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form=UsuarioCreateForm() 
        context={ #Diccionario
          'form':form,
          'title':'Creación de un Usuario',
          'modelo':'Usuarios',
          'url_lista':reverse_lazy('srea:principal'), 
         'action':'add'
        }
        
        return render(request, './usuario/usuario_create.html', context)

    def post(self, request, *args,**kwargs):
        data ={}                                     #Diccionario
        try:
            action= request.POST['action']
            if action =='add':
                form = UsuarioCreateForm(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error']=form.errors 
            else:
                data['error']='No realiza ninguna opción'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)

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
        data ={}                                     
        try:
            action= request.POST['action']
            if action =='edit':
                form = self.get_form()
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

