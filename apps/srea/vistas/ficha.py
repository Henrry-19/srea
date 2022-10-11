from django.views.generic import *
from django.contrib.auth.decorators import login_required #Importación de decoradores
from django.utils.decorators import method_decorator #Importación del método decorador
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from apps.srea.forms import FichaCreateForm
from apps.srea.models import FichaInformacion

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt

########################FichaInformacion#############################
class FichaListView(ListView):
    model = FichaInformacion
    template_name = 'ficha/ficha_lista.html'
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
                for i in FichaInformacion.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado'
        context['url_create'] = reverse_lazy('srea:ficha')
        context['url_lista'] = reverse_lazy('srea:p_ficha')
        context['modelo'] = 'FichaInformacion'
        return context

class FichaCreateView(View):
    model: FichaInformacion  #Indicar el modelo con el cual se va ha trabajar
    form= FichaCreateForm() # Indicar el formulario con el que se va ha trabajar
    template_name='./usuario/usuario_create.html' #Indicar cual es el template para crear el registro 
    success_url= reverse_lazy('srea:principal') #Me redirecciona la URL y reverse_lazy->devuelve la ruta de la URL
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form=FichaCreateForm() 
        context={ #Diccionario
          'form':form,
          'title':'Creación de una ficha',
          'modelo':'Ficha de Información',
          'url_lista':reverse_lazy('srea:p_ficha'), 
         'action':'add'
        }
        
        return render(request, './ficha/ficha_create.html', context)

    def post(self, request, *args,**kwargs):
        data ={}                                     #Diccionario
        try:
            action= request.POST['action']
            if action =='add':
                form = FichaCreateForm(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error']=form.errors 
            else:
                data['error']='No realiza ninguna opción'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)

class FichaDeleteView(DeleteView):
    model = FichaInformacion
    template_name = 'ficha/ficha_delete.html'
    success_url=reverse_lazy('srea:p_ficha')

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
        context['title'] = 'Eliminación de una ficha'
        context['modelo'] = 'Ficha de información'
        context['url_lista'] = reverse_lazy('srea:p_ficha')
        return context


class FichaUpdateView(UpdateView):
    model = FichaInformacion
    form_class = FichaCreateForm
    template_name = 'ficha/ficha_create.html'
    success_url = reverse_lazy('srea:ficha')
    
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
        context['title'] = 'Actualización de una ficha'
        context['entity'] = 'FichaInformacion'
        context['url_lista'] = reverse_lazy('srea:p_ficha')
        context['action'] = 'edit'
        return context

