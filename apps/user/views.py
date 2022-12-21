from django.views.generic import* #importando la vista genérica
from apps.srea.models import* #importando los modelos
from apps.user.models import* #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


from apps.srea.forms import*


class UserListView(ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= User#Primero se indica el modelo o entidad
    template_name = 'user/user_lista.html' #Indicarle cual es la plantilla
    
    @method_decorator(csrf_exempt)#Desactivando el mecanismo de defensa de django
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                for i in User.objects.all():
                    data.append(i.toJSON())#Incrusto cada uno de mis elementos dentro de mi array
            else:
                data["error"]='Ha ocurrido un error'
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Listado de Usuarios' #Puedo enviar variables
        context['url_create']=''#reverse_lazy('srea:user')#Ruta abosluta creación de usuario
        context['url_list']=reverse_lazy('user:user_list')#Ruta abosluta lista de usuario
        context['modelo']='Usuarios'#Nombre de identidad
        return context
