from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from apps.srea.forms import NivelCreateForm
from apps.srea.models import Nivel

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


########################Nivel#################################################
class NivelListView(View):
    def get(self,request, *args, **kwargs):
        nivel = Nivel.objects.all()
        context={
            'nivel':nivel
            
        }
        return render(request, 'nivel/nivel_lista.html', context)

class NivelCreateView(View):
    def get(self, request, *args, **kwargs):
        form=NivelCreateForm()
        context={
            'form':form
        }
        
        return render(request, './nivel/nivel_create.html', context)

#Método para crear nivel 

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=NivelCreateForm(request.POST)
            if form.is_valid():
                nombre=form.cleaned_data.get('nombre')
                numero=form.cleaned_data.get('numero')
                descripcion=form.cleaned_data.get('descripcion')
                user=form.cleaned_data.get('user')
                estado=form.cleaned_data.get('estado')
                form.save()
                
        context={
            
        }
        return redirect('srea:p_nivel')

class NivelDeleteView(DeleteView):
    model=Nivel
    template_name='nivel/nivel_delete.html'
    success_url=reverse_lazy('srea:p_nivel')

class NivelUpdateView(UpdateView):
    model=Nivel
    fields=['nombre','numero','descripcion', 'user', 'estado']
    template_name='nivel/nivel_update.html'

    def get_success_url(self): # Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_nivel')
