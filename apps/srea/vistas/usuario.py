from django.contrib.auth.decorators import login_required #Importación de decoradores
from django.utils.decorators import method_decorator #Importación del método decorador
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from apps.srea.forms import UsuarioCreateForm
from apps.srea.models import Usuario

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


########################USUARIO#############################


class UsuarioListView(View):
    @method_decorator(login_required)

    def get(self,request, *args, **kwargs):
        usuario = Usuario.objects.all()
        context={
            'usuario':usuario,
            'title' :'Lista de usuarios'
            
        }
        print(context)
        return render(request, 'usuario/usuario_lista.html', context)

class UsuarioCreateView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form=UsuarioCreateForm()
        context={
            'form':form
        }
        
        return render(request, './usuario/usuario_create.html', context)

#Método para crear usuario  
        
    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=UsuarioCreateForm(request.POST, request.FILES)
            if form.is_valid():
                apellido=form.cleaned_data.get('apellido')
                nombre=form.cleaned_data.get('nombre')
                correo=form.cleaned_data.get('correo')
                clave=form.cleaned_data.get('clave')
                fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento')
                form.save()
                return redirect('srea:principal')
        else: 
            form=UsuarioCreateForm()  #Formulario sin completar
        return render(request, 'usuario/usuario_create.html', {'form':form})

# Método para eliminar usuario
class UsuarioDeleteView(DeleteView):
    model=Usuario
    template_name='usuario/usuario_delete.html'
    success_url=reverse_lazy('srea:principal')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)


class UsuarioUpdateView(UpdateView):
    model=Usuario
    fields=['nombre','apellido','correo','clave','fecha_nacimiento']
    template_name='usuario/usuario_update.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:principal')

