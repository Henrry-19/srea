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

class CuestionarioListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= Test#Primero se indica el modelo o entidad
    template_name = 'cuestionario/test_lista.html' #Indicarle cual es la plantilla
    permission_required='view_test'
    
    @method_decorator(csrf_exempt)#Mecanismo de defensa de django
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                position = 1
                if request.user.is_staff :
                    test=Test.objects.all()
                    for i in test:
                        item= i.toJSON()
                        item['position']=position
                        data.append(item)#Incrusto cada uno de mis elemntos dentro de mi array
                        position+=1
                if  not request.user.is_staff:
                    pass
            else:
                data["error"]='Ha ocurrido un error'
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Listado de Test' #Puedo enviar variables
        context['url_create']=reverse_lazy('srea:unidad_create')#Ruta abosluta creación de usuario
        #context['url_list']=reverse_lazy('srea:unidad')#Ruta abosluta lista de usuario
        context['modelo']='Unidades'#Nombre de identidad
       
        return context