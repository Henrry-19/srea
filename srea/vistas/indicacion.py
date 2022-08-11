from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from srea.forms import IndicacionCreateForm
from srea.models import Indicacion

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


########################Indicación##################################
class IndicacionListView(View):
    def get(self,request, *args, **kwargs):
        indicacion = Indicacion.objects.all()
        context={
            'indicacion':indicacion
            
        }
        return render(request, 'indicacion/indicacion_lista.html', context)



class IndicacionCreateView(View):
    def get(self, request, *args, **kwargs):
        form=IndicacionCreateForm()
        context={
            'form':form
        }
        return render(request, './indicacion/indicacion_create.html', context)

#Método para crear indicacion   

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=IndicacionCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                descripcion = form.cleaned_data.get('descripcion')
                tiempo =form.cleaned_data.get('tiempo')
                user = form.cleaned_data.get('user')
                form.save()
        context={
            
        }
        return redirect('srea:p_indicacion')
        #return render(request, 'cuenta/cuenta_create.html', context)

class IndicacionDeleteView(DeleteView):
    model=Indicacion
    template_name='indicacion/indicacion_delete.html'
    success_url=reverse_lazy('srea:p_indicacion')

class IndicacionUpdateView(UpdateView):
    model=Indicacion
    fields=['titulo','descripcion', 'user']
    template_name='indicacion/indicacion_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_indicacion')