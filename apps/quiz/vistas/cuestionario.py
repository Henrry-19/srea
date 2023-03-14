from django.views.generic import* #importando la vista genérica
from apps.quiz.models import * #importando los modelos
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
    model= Cuestionario#Primero se indica el modelo o entidad
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
                    test=Cuestionario.objects.all()
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

class CuestionarioView(ListView):
    model= Cuestionario
    template_name = 'cuestionario/main.html'

def cuestionario_view(request, pk):
    cuestionario = Cuestionario.objects.get(pk=pk)
    return render(request, 'cuestionario/cuestionario.html', {'obj':cuestionario})

def cuestionario_data_view( request, pk):
    cuestionario = Cuestionario.objects.get(pk=pk)
    preguntas = []
    for p in cuestionario.get_preguntas():
    #    print(p)
        respuestas = []
        for  r in p.get_respuestas():
    #        print(r)
           respuestas.append(r.respuesta)
        preguntas.append({str(p):respuestas})
    
    return JsonResponse({
        'data':preguntas,
        'time':cuestionario.tiempo,
    })

def is_ajax(request): #Método usado debito a que está en desuso --->request.is_ajax()
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def save_cuestionario_view(request, pk):
    #print(request.POST)
    if is_ajax(request): #reemplaza a --> request.is_ajax()
        preguntas=[]
        data = request.POST
        data_= dict(data.lists())
    
        data_.pop('csrfmiddlewaretoken')
     
        for k in data_.keys():
            #print('key: ', k)
            pregunta=Pregunta.objects.get(texto=k)
            preguntas.append(pregunta)
        #print(preguntas)

        user=request.user
        test=Cuestionario.objects.get(pk=pk)

        puntaje=0
        multipli=100/test.numero_preguntas
        resultado=[]
        respuesta_correcta=None

        for q in preguntas:
            a_selected = request.POST.get(q.texto)
            #print('select', a_selected)

            if a_selected !="":
                pregunta_respuestas = Respuesta.objects.filter(pregunta=q)
                for a in pregunta_respuestas:
                    if a_selected == a.respuesta:
                        if a.correcta:
                            puntaje +=1
                            respuesta_correcta = a.respuesta
                    else:
                        if a.correcta:
                            respuesta_correcta
                resultado.append({str(q):{'respuesta_correcta' : respuesta_correcta, 'contestada': a_selected}})
            else:
                resultado.append({str(q):'No contestada'})

        puntaje_= puntaje*multipli
        Resultado.objects.create(cuestionario=test, user=user, score=puntaje_)

        if puntaje_>= test.required_score_to_pass:
            return JsonResponse({'passed':True, 'puntaje':puntaje_, 'resultado':resultado})
        else:
            return JsonResponse({'passed':False, 'puntaje':puntaje_, 'resultado':resultado})