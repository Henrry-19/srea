from gc import get_objects
from multiprocessing import context
from django.views.generic import View, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required #Importación de decoradores
from django.utils.decorators import method_decorator #Importación del método decorador
from django.urls import reverse_lazy

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from apps.srea.forms import *


from urllib import request
from venv import create
from django.shortcuts import render, redirect, get_object_or_404
from apps.srea.forms import RegistroFormulario, UsuarioLoginFormulario
from django.contrib.auth import authenticate, login, logout

from apps.srea.models import *

from django.conf import settings
from django.template.loader import get_template

def inicio(request):
    context={
        'bienvenido':'Bienvenido'
    }

    return render(request, 'pregunta/pregunta_lista.html',context)


def HomeUsuario(request):
    return render(request, 'pregunta/pregunta_lista.html')

#ListarPregunta
########################Pregunta#############################
class PreguntaListView(View):
    def get(self,request, *args, **kwargs):
        pregunta = Pregunta.objects.all()
        context={
            'pregunta':pregunta,
            'title' :'Pregunta'
            
        }
        return render(request, 'pregunta/pregunta_lista.html', context)


class PreguntaView(View):
    def get(self, request, *args, **kwargs):
        form=PreguntaCreateForm
        context={
            'form':form
        }
        
        return render(request, './pregunta/pregunta_create.html', context)

#Método para crear pregunta

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=PreguntaCreateForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('srea:p_pregunta')
        else:
            form:PreguntaCreateForm()   
        return render(request, 'pregunta/pregunta_create.html',  {
        'form': form
        })   



def evaluar(request): #Jugar
    QuizUser, created = Usuario2.objects.get_or_create(usuario=request.user)
    if request.method =='POST': #Si nuestro método de petición es igual a POST
        pregunta__pk = request.POST.get('pregunta__pk')
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta__pk) 
        respuesta__pk = request.POST.get('respuesta__pk')
        try:
            opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta__pk)
        except ObjectDoesNotExist:
            raise Http404

        QuizUser.validar_intento(pregunta_respondida,opcion_seleccionada) #Creando el intento
        
        return redirect('resultado', pregunta_respondida.pk)

    else:
        pregunta=QuizUser.obtener_nuevas_preguntas() #
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)
        context ={
            'pregunta':pregunta
        }

    return render(request, 'pregunta/pregunta_lista.html', context) 

def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)
    context = {
        'respondida':respondida
    }

    return render(request, 'pregunta/resultado.html', context) 
#Método de Inicio de sesión

def login2(request):
    titulo = 'login'
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect('srea:HomeUsuario')

    context = {
        'form':form,
        'title' : 'titulo' 

    }
    return render(request, 'usuario2/login.html', context)

#Creación de una cuenta

def registro(request):
    titulo = 'Crea una cuenta'
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroFormulario()
    
    context={
         'form':form,
         'title':titulo
    }

    return render(request, 'usuario2/registro.html', context)

#Método para salir del login
def logout_vista(request):
    logout(request)
    return redirect('login')