from django.views.generic import* #importando la vista genérica
from django.contrib.auth.decorators import login_required
from django.http import *
from django.urls import reverse_lazy
from apps.srea.mixins import*
from apps.srea.forms import*
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator #importando el método decorador
from django.views.decorators.csrf import csrf_exempt

class CategoriaListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= Categoria#Primero se indica el modelo o entidad
    template_name = 'categoria/categoria_lista.html' #Indicarle cual es la plantilla
    permission_required='view_categoria'
    
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
                for i in Categoria.objects.all():
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
        context['title']='Listado de categorias' #Puedo enviar variables
        #context['url_create']=reverse_lazy('srea:r_curso')#Ruta abosluta creación de matrícula
        #context['list_url']=reverse_lazy('srea:curso')#Ruta abosluta lista de usuario
        context['date_now']=datetime.now() #Se obtiene la fecha de hoy
        context['modelo']='Ciclo'#Nombre de identidad
        return context
