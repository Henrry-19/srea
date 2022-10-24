from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from apps.srea.forms import AsignaturaCreateForm
from apps.srea.models import Asignatura

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt



########################Asignatura###########################################
class AsignaturaListView(ListView):
    model = Asignatura
    template_name = 'asignatura/asignatura_lista.html'
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
                for i in Asignatura.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de asignaturas'
        context['url_create'] = reverse_lazy('srea:asignatura')
        context['url_lista'] = reverse_lazy('srea:p_asignatura')
        context['modelo'] = 'Asignatura'
        return context

class AsignaturaCreateView(View):
    model: Asignatura  #Indicar el modelo con el cual se va ha trabajar
    form= AsignaturaCreateForm() # Indicar el formulario con el que se va ha trabajar
    template_name='./usuario/usuario_create.html' #Indicar cual es el template para crear el registro 
    success_url= reverse_lazy('srea:principal') #Me redirecciona la URL y reverse_lazy->devuelve la ruta de la URL
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form=AsignaturaCreateForm() 
        context={ #Diccionario
          'form':form,
          'title':'Creación de una asignatura',
          'modelo':'Asignatura',
          'url_lista':reverse_lazy('srea:p_asignatura'), 
         'action':'add'
        }
        
        return render(request, './asignatura/asignatura_create.html', context)

    def post(self, request, *args,**kwargs):
        data ={}                                     #Diccionario
        try:
            action= request.POST['action']
            if action =='add':
                form = AsignaturaCreateForm(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error']=form.errors 
            else:
                data['error']='No realiza ninguna opción'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)

class AsignaturaDeleteView(DeleteView):
    model = Asignatura
    template_name = 'asignatura/asignatura_delete.html'
    success_url=reverse_lazy('srea:p_asignatura')

    #@method_decorator(login_required)
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
        context['title'] = 'Eliminación de una asignatura'
        context['modelo'] = 'Asignatura'
        context['url_lista'] = reverse_lazy('srea:p_asignatura')
        return context

class AsignaturaUpdateView(UpdateView):
    model = Asignatura
    form_class = AsignaturaCreateForm
    template_name = 'asignatura/asignatura_create.html'
    success_url = reverse_lazy('srea:asignatura')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}                                     
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
        context['title'] = 'Actualización de una asignatura'
        context['entity'] = 'Asignatura'
        context['url_lista'] = reverse_lazy('srea:p_asignatura')
        context['action'] = 'edit'
        return context
