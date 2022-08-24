from multiprocessing import context
from django.views.generic import View, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required #Importación de decoradores
from django.utils.decorators import method_decorator #Importación del método decorador
from django.urls import reverse_lazy

from urllib import request
from venv import create
from django.shortcuts import render, redirect
from apps.srea.forms import RegistroFormulario, UsuarioLoginFormulario
from django.contrib.auth import authenticate, login, logout

from apps.srea.models import Pregunta, PreguntasRespondidas, Usuario2

def inicio(request):
    context={
        'bienvenido':'Bienvenido'
    }

    return render(request, 'pregunta/pregunta_lista.html',context)

class PreguntaListView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        pregunta = Pregunta.objects.all()
        context={
            'pregunta':pregunta
            
        }
        return render(request, 'pregunta/pregunta_lista.html', context)


def HomeUsuario(self,request,*args, **kwargs):
   
        return render(request, 'pregunta/pregunta_lista.html')


def evaluar(request):
    evalUsuario, create = Usuario2.objects.get_or_create(usuario=request.user)
    if request.method =='POST': #Si nuestro método de petición es igual a POST
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida= evalUsuario.intentos.select_related('pregunta').get(pregunta_pk=pregunta_pk) 
        respuesta_pk = request.POST.get('respuesta_pk')
    else:
        respondidas= PreguntasRespondidas.objects.filter(quizUsuario=evalUsuario).values_list('pregunta__pk', flat=True) #Filtramos todas preguntas que ya han sido respondidas
        pregunta = Pregunta.objects.exclude(pk__in=respondidas) #Excluimos la pregunta
        context ={
            'pregunta':pregunta
        }

    return render(request, 'pregunta/pregunta_lista.html', context) 
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
         'title':'Creación de un usuario',
    }

    return render(request, 'usuario2/registro.html', context)

#Método para salir del login
def logout_vista(request):
    logout(request)
    return redirect('login')