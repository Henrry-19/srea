from django.views.generic import* #importando la vista genérica
from apps.srea.models import* #importando los modelos
from apps.user.models import* #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from apps.user.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.srea.mixins import*
from apps.srea.forms import*
from django.contrib.auth.models import Group


class UserListView(LoginRequiredMixin,IsSuperuserMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= User#Primero se indica el modelo o entidad
    template_name = 'user/user_lista.html' #Indicarle cual es la plantilla
    
    @method_decorator(csrf_exempt)#Desactivando el mecanismo de defensa de django
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            action=request.POST['action']
            if action == 'searchdata':
                data=[]
                position = 1
                for i in User.objects.all():
                    item= i.toJSON()
                    item['position']=position
                    data.append(item)#Incrusto cada uno de mis elementos dentro de mi array
                    position+=1
            else:
                data["error"]='Ha ocurrido un error'
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Listado de Usuarios' #Puedo enviar variables
        context['url_create']=reverse_lazy('user:user')#Ruta abosluta creación de usuario
        context['url_list']=reverse_lazy('user:user_list')#Ruta abosluta lista de usuario
        context['modelo']='Usuarios'#Nombre de identidad
        return context


class UserCreateView(CreateView):
    model=User #Indicar el modelo con el cual se va ha trabajar
    form_class=UserCreateForm #Importando el formulario con el que voy a trabajar
    template_name='user/user_create.html' # Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('user:user_list') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro

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
        context['title']='Creación de un usuario' #Puedo enviar variables
        context['modelo']='User'#Nombre de identidad
        context['url_list']=self.success_url#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context

class UserUpdateView(UpdateView):
    model = User #Indicar el modelo con el cual se va ha trabajar
    form_class = UserCreateForm #Importando el formulario con el que voy a trabajar
    template_name = 'user/user_create.html' #Debo indicarle la ubicación de mi plantilla
    success_url = reverse_lazy('user:user_list') #Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    #@method_decorator(csrf_exempt) #Mecanismo de defensa de django
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()#Le decimos que la clase object va a hacer igual a lo que tenemos en lainstancia de nuestro objeto, para que el funcionamiento no se altere
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data ={}                                     
        try:
            action= request.POST['action']
            if action =='edit':
                form = self.get_form()
                data=form.save()
            else:
                data['error']='No realiza ninguna acción'
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)
        
    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Actualización de un usuario' #Puedo enviar variables
        context['modelo']='User'#Nombre de identidad
        context['url_list']=self.success_url#Ruta abosluta lista de asignatura
        context['action']='edit'#Enviar variable action
        return context

class UserDeleteView(DeleteView):
    model = User #Indicar el modelo con el cual se va ha trabajar
    template_name = 'user/user_delete.html' #Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('user:user_list')#Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    
   
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() #Le decimos que la clase object va a hacer igual a lo que tenemos en lainstancia de nuestro objeto, para que el funcionamiento no se altere
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {} #Creación de variable tipo diccionario
        try:
            self.object.delete()#La variabe self.object contiene la variable de mi objeto y puedo acceder a los métodos
        except Exception as e:
            data['error'] = str(e) # Si llega a ocurrir un error de la excepion se debe guaradar en la viable e
        return JsonResponse(data) #Retorno como respuesta un JsonResponse
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un usuario'
        context['modelo'] = 'User'
        context['url_list'] = self.success_url
        return context

class UserChangeGroup(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk']) #Guardo la sesión que voy a utilizar
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('srea:index1'))