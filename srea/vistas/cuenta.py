from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from srea.forms import CuentaCreateForm
from srea.models import Cuenta

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



class sreaListView(View):
    def get(self,request, *args, **kwargs):
        cuenta = Cuenta.objects.all()
        context={
            'cuenta':cuenta,
            'title' :'Lista de cuentas'
            
        }
        return render(request, 'cuenta/srea_lista.html', context)



class CuentaCreateView(View):
    def get(self, request, *args, **kwargs):
        form=CuentaCreateForm()
        context={
            'form':form,
            'title' :'Creación de una cuenta'
        }
        return render(request, './cuenta/cuenta_create.html', context)

#Método para crear cuenta    

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si el usuario está enviando el formulario con datos
            form=CuentaCreateForm(request.POST)
            if form.is_valid():
                correo = form.cleaned_data.get('correo')
                clave = form.cleaned_data.get('clave')
                estado =form.cleaned_data.get('estado')
                user = form.cleaned_data.get('user')
                form.save() #Guardar los datos en la base de datos
                return redirect('srea:home')
        else: 
            form=CuentaCreateForm()  #Formulario sin completar
        return render(request, 'cuenta/cuenta_create.html', {'form':form})

#Método para actualizar la información
class CuentaUpdateView(UpdateView):
    model=Cuenta
    fields=['correo','clave','estado', 'user']
    template_name='cuenta/cuenta_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:home')


#Método para eliminar la información

class CuentaDeleteView(DeleteView):
    model=Cuenta
    template_name='cuenta/cuenta_delete.html'
    success_url=reverse_lazy('srea:home')