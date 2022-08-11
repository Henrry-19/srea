from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from srea.forms import FichaCreateForm
from srea.models import FichaInformacion

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

########################FichaInformacion#############################
class FichaListView(View):
    def get(self,request, *args, **kwargs):
        ficha = FichaInformacion.objects.all()
        context={
            'ficha':ficha
            
        }
        return render(request, 'ficha/ficha_lista.html', context)

class FichaCreateView(View):
    def get(self, request, *args, **kwargs):
        form=FichaCreateForm()
        context={
            'form':form
        }
        return render(request, './ficha/ficha_create.html', context)

#Método para crear ficha

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=FichaCreateForm(request.POST)
            if form.is_valid():
                descripcion = form.cleaned_data.get('descripcion')
                detalle_trabajo = form.cleaned_data.get('detalle_trabajo')
                detalle_ocupacion = form.cleaned_data.get('detalle_ocupacion')
                detalle_tecnicaE = form.cleaned_data.get('detalle_tecnicaE')
                genero= form.cleaned_data.get('genero')
                etnia=form.cleaned_data.get('etnia')
                estado_civil=form.cleaned_data.get('estado_civil')
                user = form.cleaned_data.get('user')
                form.save()
        context={
            
        }
        return redirect('srea:p_ficha')

class FichaDeleteView(DeleteView):
    model=FichaInformacion
    template_name='ficha/ficha_delete.html'
    success_url=reverse_lazy('srea:p_ficha')
class FichaUpdateView(UpdateView):
    model=FichaInformacion
    fields=['descripcion','detalle_trabajo', 'detalle_ocupacion', 'genero', 'etnia', 'estado_civil','user']
    template_name='ficha/ficha_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_ficha')
