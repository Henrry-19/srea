from django.views.generic import* #importando la vista genérica
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from apps.srea.mixins import*

from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin

#############################################################
from apps.srea.models import*
import random
#############################################################

class TestListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= Test #Primero se indica el modelo o entidad
    template_name = 'test/test_lista.html' #Indicarle cual es la plantilla
    #permission_required='view_asignatura'
    
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
                for i in Test.objects.all():
                    item= i.toJSON()
                    item['position']=position
                    data.append(item)#Incrusto cada uno de mis elemntos dentro de mi array
                    position+=1
            else:
                data["error"]='Ha ocurrido un error'
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Listado de test' #Puedo enviar variables
        #context['url_create']=reverse_lazy('srea:asignatura')#Ruta abosluta creación de usuario
        #context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de usuario
        context['modelo']='Test'#Nombre de identidad
        return context


def get_test(request): ###Métod para obtner el test
    try:
        pregunta_objs= list(Pregunta.objects.all())
        data = []
        random.shuffle(pregunta_objs)
        for pregunta_obj  in pregunta_objs:
            data.append({
                'test':pregunta_obj.test.titulo,
                'pregunta':pregunta_obj.pregunta,
                'tipoPregunta':pregunta_obj.tipoPregunta,
                'respuesta':pregunta_obj.get_respuestas()
            })
        payload={'status':True, 'data' : data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
    return HttpRequest("Existe un error")