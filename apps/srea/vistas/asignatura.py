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
            'title':'Lista de asignaturas'  
        }
        return render(request, 'asignatura/asignatura_lista.html', context)

class AsignaturaCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Asignatura #Indicar el modelo con el cual se va ha trabajar
    form_class=AsignaturaCreateForm #Importando el formulario con el que voy a trabajar
    template_name='asignatura/asignatura_create.html' # Debo indicarle la ubicación de mi plantilla
    permission_required='add_asignatura'
    success_url= reverse_lazy('srea:asignatura') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro

   
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
         user = request.user
         if request.method == 'POST':
              form = AsignaturaCreateForm(request.POST, request.FILES)
              #print(form)
              if form.is_valid():
                   ciclo = form.cleaned_data.get('ciclo')
                   nombre = form.cleaned_data.get('nombre')
                   detalle = form.cleaned_data.get('detalle')
                   imagen = form.cleaned_data.get('imagen')
                   Asignatura.objects.create(ciclo=ciclo, nombre=nombre, detalle=detalle,imagen=imagen, docente=user)
                   return redirect('srea:p_asignatura')
         else:
            form=AsignaturaCreateForm()
         context = {
		        'form': form,
                'list_url':reverse_lazy('srea:p_asignatura')
	     }
         return render(request, 'asignatura/asignatura_create.html', context)

class AsignaturaUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model=Asignatura
    form_class = AsignaturaCreateForm
    permission_required='change_asignatura'
    template_name='asignatura/asignatura_create.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_asignatura')


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
def Enroll(request, asignatura_id, user_id):
    #user = request.user
    usuarios= User.objects.all()
    course = get_object_or_404(Asignatura, id=asignatura_id)
    user=get_object_or_404(User,id=user_id)
    #course = get_object_or_404(User, id=user_id)
    if request.user.is_staff :
        course.users.add(user)
    #return redirect('srea:matricula-lista', asignatura_id=asignatura_id, user_id=user_id)
    return redirect('srea:p_asignatura')