from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.contrib.auth.decorators import login_required
from django.http import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from apps.srea.mixins import*
from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

#############################################UNIDAD##############################################################
@login_required
@permission_required('srea.view_unidad')
def AsignaturaUnidades(request, asignatura_id):
    #user=request.user
    course=get_object_or_404(Asignatura, id=asignatura_id)
   

    
    context = {
        'course':course,
    }
    return render(request, 'unidad/unidades.html', context)

@login_required
@permission_required('srea.add_unidad')
def NewModule(request, asignatura_id):
    course = get_object_or_404(Asignatura, id=asignatura_id)#calculo
    if not request.user.is_staff :
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = UnidadCreateForm(request.POST, request.FILES)
            if form.is_valid():
                nombre=form.cleaned_data.get('nombre')
                descripcion=form.cleaned_data.get('descripcion')
                m = Unidad.objects.create(nombre=nombre,descripcion=descripcion)# en docente registramos directamente en launidad
                #print("mmm-->",m)
                course.unidad.add(m)# registramos la unidad en la asignatura
                course.save()
                return redirect('srea:primeraU', asignatura_id=asignatura_id)
        else:
            form = UnidadCreateForm()
    context = {
		'form': form,
        'asignatura_id':asignatura_id,
        'course':course,
        'url_list':reverse_lazy('srea:p_asignatura')
	}
    return render(request, 'unidad/newmodule.html', context)

@login_required
@permission_required('srea.change_unidad')
def EditMudule(request, unidad_id, asignatura_id):#Editar unidad
    course = get_object_or_404(Unidad, id=unidad_id)
    #if request.user.is_staff:
    if request.method == 'POST':
        form = UnidadEditarCreateForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course.nombre = form.cleaned_data.get('nombre')
            course.descripcion = form.cleaned_data.get('descripcion')
                #quizzes=form.cleaned_data.get('quizzes')
                #quiz=Quiz.objects.filter(quizzes=quizzes)
                #print(quizzes)
                #course.quizzes.set(quiz)
                #form.save()
            course.save()
                #form=self.get_form() #Llamamos a nuestro formulario
                #if form.is_valid():# Preguntamos si nuestro formulario es valido
                   
            return redirect('srea:primeraU', asignatura_id=asignatura_id)
    else:
        form = UnidadEditarCreateForm(instance=course)
    context = {
		'form': form,
		'course': course,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'unidad/newmodule.html', context)

class UnidadDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Unidad #Indicar el modelo con el cual se va ha trabajar
    template_name = 'unidad/unidad_delete.html' #Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('srea:unidad')#Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    permission_required='delete_unidad'
 
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
        context['title'] = 'Eliminación de una unidad'
        context['modelo'] = 'Unidad'
        context['url_list'] = reverse_lazy('srea:p_asignatura')
        return context

@login_required
@permission_required('quiz.add_quiz')
def RegistrarQuiz(request, asignatura_id):
    asigna = get_object_or_404(Asignatura, id=asignatura_id)
    if request.method == 'POST':
        form = RegistrarQuizForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            quiz=form.cleaned_data.get('quiz')
            unidad=form.cleaned_data.get('unidad')
            m = UnidadQuiz.objects.create(quiz=quiz,unidad=unidad)
            m.save()
            return redirect('srea:primeraU', asignatura_id=asignatura_id)
    else:
        form = RegistrarQuizForm(request=request)

        context = {
		'form': form,
        'asignatura_id':asignatura_id,
        'asigna':asigna,
        #'url_list':reverse_lazy('srea:p_asignatura')
	    }
        return render(request, 'unidad/registrar_quiz.html', context)
