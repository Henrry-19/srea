from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from apps.srea.mixins import*
import uuid
from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from apps.srea.encryption_util import*

class AsignaturaListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,View):
    model= Asignatura
    template_name = 'asignatura/asignatura_lista.html'
    permission_required='view_asignatura'
    def get(self,request, *args, **kwargs):
        user=request.user
        if request.user.is_staff : 
            asignatura = Asignatura.objects.all()
        if  not request.user.is_staff:
            asignatura = Asignatura.objects.filter(users=user)

        context={
            'asignatura':asignatura,
            'url_create':reverse_lazy('srea:asignatura'),
            'list_url':reverse_lazy('srea:p_asignatura'),
            'title':'Lista de asignaturas',
            'modelo':'Asignaturas',
            'date_now':datetime.now()  
        }

        return render(request, 'asignatura/asignatura_lista.html', context)
    
    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Lista de asignaturas' #Puedo enviar variables
        context['url_create']=reverse_lazy('srea:asignatura')#Ruta abosluta creación de usuario
        context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de usuario
        context['modelo']='Asignaturas'#Nombre de identidad
        return context

##Este método no sirve
class AsignaturaCreateView2(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Asignatura #Indicar el modelo con el cual se va ha trabajar
    form_class=AsignaturaCreateForm #Importando el formulario con el que voy a trabajar
    template_name='asignatura/asignatura_create.html' # Debo indicarle la ubicación de mi plantilla
    permission_required='add_asignatura'
    success_url= reverse_lazy('srea:asignatura') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro

   
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
         #user = request.user
        data={}
        try:
            action= request.POST['action']
            if action=='add':
                form=self.get_form() #Llamamos a nuestro formulario
                if form.is_valid():
                    form.save()
                    return redirect('srea:p_asignatura')
                else:
                    data['error']=form.errors # Data va a hacer igual al formulario con los errores 
            else:
                data['error']='No ingreso por ninguna opción'
        except Exception as e:
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return HttpResponse(data) 
    

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Creación de una Asignatura' #Puedo enviar variables
        context['modelo']='Asignatura'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context

        #return render(request, 'asignatura/asignatura_create.html', context)


##Este método sirve
class AsignaturaCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Asignatura #Indicar el modelo con el cual se va ha trabajar
    form_class=AsignaturaCreateForm #Importando el formulario con el que voy a trabajar
    template_name='asignatura/asignatura_create.html' # Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('srea:asignatura') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro
    permission_required='add_asignatura'
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
        context['title']='Creación de una Asignatura' #Puedo enviar variables
        context['modelo']='Asignatura'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context


##Este método sirve
class AsignaturaUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Asignatura #Indicar el modelo con el cual se va ha trabajar
    form_class = AsignaturaModificarCreateForm #Importando el formulario con el que voy a trabajar
    template_name = 'asignatura/asignatura_create.html' #Debo indicarle la ubicación de mi plantilla
    permission_required='change_asignatura'
    success_url = reverse_lazy('srea:p_asignatura') #Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
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
        context['title']='Actualización de una Asignatura' #Puedo enviar variables
        context['modelo']='Asignatura'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de asignatura
        context['action']='edit'#Enviar variable action
        return context


##Este método no sirve
class AsignaturaUpdateView2(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model=Asignatura
    form_class = AsignaturaCreateForm
    permission_required='change_asignatura'
    template_name='asignatura/asignatura_create.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_asignatura')
    
    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Editar Asignatura' #Puedo enviar variables
        context['modelo']='Asignatura'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de asignatura
        return context


class AsignaturaDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Asignatura #Indicar el modelo con el cual se va ha trabajar
    template_name = 'asignatura/asignatura_delete.html' #Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('srea:p_asignatura')#Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    permission_required='delete_asignatura'
 
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
        context['title'] = 'Eliminación de una asignatura'
        context['modelo'] = 'Asignatura'
        context['url_list'] = reverse_lazy('srea:p_asignatura')
        return context


@login_required
def AsignaturaDetail(request, asignatura_id):
        #asignatura_pk=decrypt(asignatura_pk)
        user = request.user
        asigna = get_object_or_404(Asignatura, id=asignatura_id)
        teacher_mode=False
        #print(asigna.unidad)
        if user == asigna.docente:
            teacher_mode = True
        context = {
            'asigna': asigna,
            'teacher_mode': teacher_mode,
            'modelo':'Asignaturas'
        }

        return render(request, 'asignatura/courses.html', context)

@login_required
def ListarEstudiantes(request, asignatura_id):
        user = request.user
        #print(user)
        lista = get_object_or_404(Asignatura, id=asignatura_id)
        #print(lista)
        context = {
                    'lista': lista,
                    'title':'Participantes', #Puedo enviar variables
                    'asignatura_id':asignatura_id
        }

        return render(request, 'asignatura/asignatura_lista_estudiantes.html', context)


@login_required
def MatricularLista(request, asignatura_id, user_id):
    #user = request.user
    usuarios= User.objects.all()
    user=get_object_or_404(User,id=user_id)
    asignatura=get_object_or_404(Asignatura, id=asignatura_id)
    #course.enrolled.add(user)
    context= {
          'usuarios':usuarios,
          'title':'Matrícular en la asignatura: ',
          'asignatura_id':asignatura_id,
          'asignatura':asignatura,
          'user':user
    }
    return render(request, 'asignatura/matricular_estudiantes.html', context)   

@login_required
def Enroll(request, asignatura_id, user_id):#Matricular estudiantes
    #user = request.user
    usuarios= User.objects.all()
    course = get_object_or_404(Asignatura, id=asignatura_id)
    user=get_object_or_404(User,id=user_id)
    #course = get_object_or_404(User, id=user_id)
    if request.user.is_staff :
        course.users.add(user)
    #return redirect('srea:matricula-lista', asignatura_id=asignatura_id, user_id=user_id)
    return redirect('srea:p_asignatura')


