from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from apps.srea.mixins import*

from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin

class RespuestaCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Respuesta #Indicar el modelo con el cual se va ha trabajar
    form_class=PreguntaCreateForm #Importando el formulario con el que voy a trabajar
    template_name='respuesta/respuesta_create.html' # Debo indicarle la ubicación de mi plantilla
    #permission_required='add_pregunta'
    success_url= reverse_lazy('srea:pregunta') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro

   
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            action= request.POST['action']#Recupero la variable action en mi método POST, cada vez que se haga una petición
            if action=='add': #Se indica el proceso add
                form=self.get_form() #Llamamos a nuestro formulario
                if form.is_valid():# Preguntamos si nuestro formulario es valido
                    form.save()#Debo guardar el objeto
                else:
                    data['error']=form.errors # Data va a hacer igual al formulario con los errores 
            else:
                data['error']='No ingreso por ninguna opción'
        except Exception as e: #Llamamos a la clase Exception para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data)


    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Creación de una respuesta' #Puedo enviar variables
        context['modelo']='Respuesta'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:pregunta')#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context