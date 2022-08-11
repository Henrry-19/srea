from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from srea.forms import PreguntaCreateForm
from srea.models import Pregunta

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


########################Pregunta##############################################

class PreguntaListView(View):
    def get(self,request, *args, **kwargs):
        pregunta = Pregunta.objects.all()
        context={
            'pregunta':pregunta
            
        }
        return render(request, 'pregunta/pregunta_lista.html', context)

class PreguntaCreateView(View):
    def get(self, request, *args, **kwargs):
        form=PreguntaCreateForm()
        context={
            'form':form
        }
        
        return render(request, './pregunta/pregunta_create.html', context)

#Método para crear pregunta
    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=PreguntaCreateForm(request.POST)
            if form.is_valid():
                pregunta=form.cleaned_data.get('pregunta')
                user=form.cleaned_data.get('user')
                estado=form.cleaned_data.get('estado')
                form.save()
                
        context={
            
        }
        return redirect('srea:p_pregunta')


class PreguntaDeleteView(DeleteView):
    model=Pregunta
    template_name='pregunta/pregunta_delete.html'
    success_url=reverse_lazy('srea:p_pregunta')


class PreguntaUpdateView(UpdateView):
    model=Pregunta
    fields=['pregunta', 'user', 'estado']
    template_name='pregunta/pregunta_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_pregunta')