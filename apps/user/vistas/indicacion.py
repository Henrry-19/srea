from django.shortcuts import render
from apps.user.models import*
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.srea.mixins import*
from django.views.generic import* #importando la vista genérica
from django.http import *
from apps.user.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from apps.srea.models import*
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

class IndicacionListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,View):
    model= Indicacion
    template_name = 'ayuda/ayuda.html'
    permission_required='view_indicacion'
    def get(self,request, *args, **kwargs):
        user=request.user
        #print(user.groups.all())
        if request.user.is_staff : 
            indicacion = Indicacion.objects.all()
        if  not request.user.is_staff:
            indicacion = Indicacion.objects.all()

        context={
            'indicacion':indicacion,
            #'url_create':reverse_lazy('user:indicacion'),
            'list_url':reverse_lazy('user:ayuda'),
            'title':'Lista de ayuda',
            'modelo':'Ayuda',
            'date_now':datetime.now()  
        }

        return render(request, 'ayuda/ayuda.html', context)
    
@login_required
@permission_required('user.view_indicacion')
def IndicacionAsignatura(request, asignatura_id):
    user=request.user
    asigna = get_object_or_404(Asignatura, id=asignatura_id)
   
        #print(user.groups.all())
    asignatura=Asignatura.objects.filter(users=user)
    print('---->',asignatura)
    if request.user.is_staff : 
        indicacion = Indicacion.objects.all()
    if  not request.user.is_staff:
        for u in user.groups.all():
            print(u.id)
        indicacion = Indicacion.objects.filter(user_indicacion=user)

    context={
            'indicacion':indicacion,
            'url_create':reverse_lazy('user:indicacion'),
            'list_url':reverse_lazy('user:mensaje'),
            'title':'Lista de indicaciones',
            'modelo':'Indicaciones',
            'date_now':datetime.now()  
    }

    return render(request, 'indicacion/indicacion_lista.html', context)
    

class IndicacionCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Indicacion #Indicar el modelo con el cual se va ha trabajar
    form_class=IndicacionCreateForm #Importando el formulario con el que voy a trabajar
    template_name='indicacion/indicacion_create.html' # Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('user:mensaje') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro
    permission_required='add_indicacion'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            action= request.POST['action']#Recupero la variable action en mi método POST, cada vez que se haga una petición
            if action=='add': #Se indica el proceso add
                form=self.get_form() #Llamamos a nuestro formulario
                if form.is_valid():# Preguntamos si nuestro formulario es valido
                    form.save()
                else:
                    data['error']=form.errors # Data va a hacer igual al formulario con los errores 
            else:
                data['error']='No ingreso por ninguna opción'
        except Exception as e: #Llamamos a la clase Exception para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data)


    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Creación de una Indicación' #Puedo enviar variables
        context['modelo']='Indicación'#Nombre de identidad
        context['url_list']=reverse_lazy('user:mensaje')#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context


def AyudaLista(request, indicacion_id):
    indi=get_object_or_404(Indicacion, id=indicacion_id)
    print(indi)

    context = {
        'indi':indi,
    }
    return render(request, 'ayuda/ayuda.html', context)
