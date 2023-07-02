from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from apps.srea.mixins import*

from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from apps.srea.encryption_util import*
from django.contrib.auth.decorators import permission_required

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

@login_required
@permission_required('srea.change_asignatura')
def AsignaturaUpdateView(request, asignatura_id):#Editar asignatura
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    #if request.user.is_staff:
    if request.method == 'POST':
        form = AsignaturaModificarCreateForm(request.POST, request.FILES, instance=asignatura)
        if form.is_valid():
            asignatura.nombre = form.cleaned_data.get('nombre')
            asignatura.descripcion = form.cleaned_data.get('descripcion')
                #users=form.cleaned_data.get('users')
                #user=User.objects.filter(users=users)
                #print(users)#---->ojo
                #asignatura.users.set(user)
            asignatura.save()   
            return redirect('srea:p_asignatura')
    else:
        form = AsignaturaModificarCreateForm(instance=asignatura)

    context = {
		'form': form,
		'course': asignatura,
        'asignatura_id':asignatura_id,
        'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'asignatura/asignatura_prueba.html', context)

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
@permission_required('srea.view_asignatura')
def AsignaturaDetail(request, asignatura_id):
        asigna = get_object_or_404(Asignatura, id=asignatura_id)
        teacher_mode = False
        user=request.user
        for g in user.groups.all():
                if g.name == "Docente":
                   teacher_mode = True
                   print("---->",teacher_mode)
                   
        
        context = {
            'asigna': asigna,
            'teacher_mode': teacher_mode,
            'modelo':'Asignaturas'
        }
        
        return render(request, 'asignatura/courses.html', context)

@login_required
@permission_required('user.view_user')
def ListarEstudiantes(request, asignatura_id):
        lista = get_object_or_404(Asignatura, id=asignatura_id)
        context = {
                    'lista': lista,
                    'title':'Participantes', #Puedo enviar variables
                    'asignatura_id':asignatura_id
        }

        return render(request, 'asignatura/asignatura_lista_estudiantes.html', context)


@login_required
@permission_required('user.add_user')
def MatricularLista(request, asignatura_id, user_id):
    #user = request.user
    usuarios= User.objects.all()
    user=get_object_or_404(User,id=user_id)
    asignatura=get_object_or_404(Asignatura, id=asignatura_id)
    #course.enrolled.add(user)
    context= {
          'usuarios':usuarios,
          'title':'Registrar en la asignatura: ',
          'asignatura_id':asignatura_id,
          'asignatura':asignatura,
          'user_id':user_id
    }
    return render(request, 'asignatura/matricular_estudiantes.html', context)   

@login_required
@permission_required('user.add_user')
def Matricular(request, asignatura_id, user_id):#Matricular estudiantes
    #user = request.user
    course = get_object_or_404(Asignatura, id=asignatura_id)
    #use=get_object_or_404(User,id=user_id)
    #course = get_object_or_404(User, id=user_id)
    #if request.user.is_staff :
    if request.method=='POST':
        user= request.POST.getlist('usuarios')
        

    for u in (user):
        #print('TOBY---->',u)
        course.users.add(u)

    return redirect('srea:estudiantes', asignatura_id=asignatura_id)
    #return redirect('srea:p_asignatura')




