from email import message
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

#from srea.util import render_to_pdf
from .forms import CuentaCreateForm, UsuarioCreateForm, ReporteCreateForm, IndicacionCreateForm,FichaCreateForm, AsignaturaCreateForm, NivelCreateForm, TestCreateForm, PreguntaCreateForm  
from .models import Cuenta, Usuario, Reporte, FichaInformacion, Indicacion, Asignatura, Nivel, Test, Pregunta
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
            'cuenta':cuenta
            
        }
        return render(request, 'cuenta/srea_lista.html', context)



class CuentaCreateView(View):
    def get(self, request, *args, **kwargs):
        form=CuentaCreateForm()
        context={
            'form':form
        }
        return render(request, './cuenta/cuenta_create.html', context)

#Método para crear cuenta    

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=CuentaCreateForm(request.POST)
            if form.is_valid():
                correo = form.cleaned_data.get('correo')
                clave = form.cleaned_data.get('clave')
                estado =form.cleaned_data.get('estado')
                user = form.cleaned_data.get('user')

                C, created=Cuenta.objects.get_or_create(correo=correo,clave=clave,estado=estado, user=user)
                C.save()
                return redirect('srea:home')
        context={
            
        }
        
        return render(request, 'cuenta/cuenta_create.html', context)

#Método para presentar la información

class CuentaDetailView(View):
    def get(self, request, pk,*args, **kwargs):
        cuenta=get_object_or_404(Cuenta, pk=pk)
        context={
            'cuenta':cuenta

        }
        return render (request, 'cuenta/cuenta_detail.html', context)

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


########################USUARIO#############################


class UsuarioListView(View):
    def get(self,request, *args, **kwargs):
        usuario = Usuario.objects.all()
        context={
            'usuario':usuario

            
        }
        print(context)
        return render(request, 'usuario/usuario_lista.html', context)

class UsuarioCreateView(View):
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
                cedula=form.cleaned_data.get('cedula')
                apellido=form.cleaned_data.get('apellido')
                nombre=form.cleaned_data.get('nombre')
                fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento')
                edad=form.cleaned_data.get('edad')
                direccion=form.cleaned_data.get('direccion')
                foto=form.cleaned_data.get('foto')
                id_usuario=form.cleaned_data.get('id_usuario')
                form.save()
                
        context={
            
        }
        return redirect('srea:principal')
        #return render(request, 'usuario/usuario_create.html', context)

# Método para eliminar usuario
class UsuarioDeleteView(DeleteView):
    model=Usuario
    template_name='usuario/usuario_delete.html'
    success_url=reverse_lazy('srea:principal')

class UsuarioUpdateView(UpdateView):
    model=Usuario
    fields=['cedula','apellido','nombre', 'direccion']
    template_name='usuario/usuario_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:principal')



########################REPORTE##########################################3
class ReporteListView(View):
    def get(self,request, *args, **kwargs):
        reporte = Reporte.objects.all()
        context={
            'reporte':reporte
            
        }
        return render(request, 'reporte/reporte_lista.html', context)

#Reporte en pdf
class ReporteListPdf(View):
    def get(self,request, *args, **kwargs):
        try:
            template = get_template("reporte/reporte_imprimir.html")
            reporte=Reporte.objects.all()
            #reporte=Reporte.objects.get(pk=self.kwargs['pk'])
            context = {
                #'reporte': Reporte.objects.get(pk=self.kwargs['pk'])
                'reporte': reporte
            }
            html=template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            pisa_status = pisa.CreatePDF(
                html, dest=response)

            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('srea:p_reporte')) 


class ReporteCreateView(View):
    def get(self, request, *args, **kwargs):
        form=ReporteCreateForm()
        context={
            'form':form
        }
        return render(request, './reporte/reporte_create.html', context)

#Método para crear reporte   

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=ReporteCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                descripcion = form.cleaned_data.get('descripcion')
                estado =form.cleaned_data.get('estado')
                user = form.cleaned_data.get('user')
                form.save()
        context={
            
        }
        return redirect('srea:p_reporte')
        #return render(request, 'cuenta/cuenta_create.html', context)

class ReporteDeleteView(DeleteView):
    model=Reporte
    template_name='reporte/reporte_delete.html'
    success_url=reverse_lazy('srea:p_reporte')

class ReporteUpdateView(UpdateView):
    model=Reporte
    fields=['titulo','descripcion','estado', 'user']
    template_name='reporte/reporte_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_reporte')

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
                detalle_tecnica_estudio = form.cleaned_data.get('detalle_tecnica_estudio')
                genero= form.cleaned_data.get('genero')
                etnia=form.cleaned_data.get('etnia')
                estado_civil=form.cleaned_data.get('estado_civil')
                user = form.cleaned_data.get('user')
                form.save()
        context={
            
        }
        return redirect('srea:p_ficha')

class FichaDeleteView(DeleteView):
    model=Test
    template_name='ficha/ficha_delete.html'
    success_url=reverse_lazy('srea:p_ficha')
class FichaUpdateView(UpdateView):
    model=FichaInformacion
    fields=['descripcion','detalle_trabajo', 'detalle_ocupacion', 'genero', 'etnia', 'estado_civil','user']
    template_name='ficha/ficha_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_ficha')


        
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

########################Asignatura###########################################
class AsignaturaListView(View):
    def get(self,request, *args, **kwargs):
        asignatura = Asignatura.objects.all()
        context={
            'asignatura':asignatura
            
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
        #return redirect('srea:p_asignatura')
        #return render(request, 'asignatura/asignatura_create.html', context)

class AsignaturaDeleteView(DeleteView):
    model=Asignatura
    template_name='asignatura/asignatura_delete.html'
    success_url=reverse_lazy('srea:p_asignatura')

class AsignaturaUpdateView(UpdateView):
    model=Asignatura
    fields=['nombre','detalle','foto', 'user', 'estado']
    template_name='asignatura/asignatura_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_asignatura')


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

    fields=['nombre','numero','descripcion', 'user', 'estado']
    template_name='nivel/nivel_update.html'

    def get_success_url(self): # Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_nivel')



########################Test##################################################

class TestListView(View):
    def get(self,request, *args, **kwargs):
        test = Test.objects.all()
        context={
            'test':test
            
        }
        return render(request, 'test/test_lista.html', context)


class TestCreateView(View):
    def get(self, request, *args, **kwargs):
        form=TestCreateForm()
        context={
            'form':form
        }
        
        return render(request, './test/test_create.html', context)

#Método para crear test
    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=TestCreateForm(request.POST)
            if form.is_valid():
                nombre=form.cleaned_data.get('nombre')
                user=form.cleaned_data.get('user')
                estado=form.cleaned_data.get('estado')
                form.save()
                
        context={
            
        }
        return redirect('srea:p_test')


class TestDeleteView(DeleteView):
    model=Test
    template_name='test/test_delete.html'
    success_url=reverse_lazy('srea:p_test')

class TestUpdateView(UpdateView):

    fields=['nombre', 'user', 'estado']
    template_name='test/test_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_test')


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

    fields=['pregunta', 'user', 'estado']
    template_name='pregunta/pregunta_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_pregunta')