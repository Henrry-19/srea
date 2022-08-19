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



########################Asignatura###########################################
class AsignaturaListView(View):
    def get(self,request, *args, **kwargs):
        asignatura = Asignatura.objects.all()
        context={
            'asignatura':asignatura,
            'title':'Lista de asignaturas'
            
        }
        return render(request, 'asignatura/asignatura_lista.html', context)

class AsignaturaCreateView(View):
    def get(self, request, *args, **kwargs):
        form=AsignaturaCreateForm()
        context={
            'form':form
        }
        
        return render(request, './asignatura/asignatura_create.html', context)

#Método para crear asignatura  

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=AsignaturaCreateForm(request.POST, request.FILES)
            if form.is_valid():
                nombre=form.cleaned_data.get('nombre')
                detalle=form.cleaned_data.get('detalle')
                foto=form.cleaned_data.get('foto')
                estado=form.cleaned_data.get('estado')
                user=form.cleaned_data.get('user')
                form.save()
                return redirect('srea:p_asignatura')
        else:
            form:AsignaturaCreateForm()   
        return render(request, 'asignatura/asignatura_create.html',  {
        'form': form
        })   


class AsignaturaDeleteView(DeleteView):
    model=Asignatura
    template_name='asignatura/asignatura_delete.html'
    success_url=reverse_lazy('srea:p_asignatura')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Asignatura'
        context['entity'] = 'Asignatura'
        context['url_lista'] = reverse_lazy('srea:p_asignatura')
        return context

class AsignaturaUpdateView(UpdateView):
    model=Asignatura
    fields=['nombre','detalle','foto','user']
    template_name='asignatura/asignatura_create.html'
    success_url = reverse_lazy('srea:p_asignatura')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualización de una Asignatura'
        context['entity'] = 'Asignatura'
        context['url_lista'] = reverse_lazy('srea:p_asignatura')
        context['action'] = 'edit'
        return context
