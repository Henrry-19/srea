from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from apps.srea.mixins import*
from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

class UnidadListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= Unidad#Primero se indica el modelo o entidad
    template_name = 'htz/body.html' #Indicarle cual es la plantilla
    permission_required='view_unidad'
    
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
                    for i in Unidad.objects.all():
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
        context['title']='Listado de Unidad' #Puedo enviar variables
        #context['url_create']=reverse_lazy('srea:unidad')#Ruta abosluta creación de usuario
        context['url_list']=reverse_lazy('srea:p_unidad')#Ruta abosluta lista de usuario
        context['modelo']='Unidades'#Nombre de identidad
        return context


class UnidadesListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= Unidad#Primero se indica el modelo o entidad
    template_name = 'unidad/unidad_list.html' #Indicarle cual es la plantilla
    permission_required='view_unidad'
    
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
                    unidad=Unidad.objects.all()
                    for i in unidad:
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
        context['title']='Listado de Unidad' #Puedo enviar variables
        context['url_create']=reverse_lazy('srea:unidad_create')#Ruta abosluta creación de usuario
        #context['url_list']=reverse_lazy('srea:unidad')#Ruta abosluta lista de usuario
        context['modelo']='Unidades'#Nombre de identidad
       
        return context

#############################################PRIMERA UNIDAD##############################################################
@login_required
def AsignaturaUnidades(request, asignatura_id):
    user=request.user
    course=get_object_or_404(Asignatura, id=asignatura_id)

    theacher_mode=False
    if user == course.docente:
       theacher_mode=True
    
    context = {
        'course':course,
        'theacher_mode':theacher_mode,
        #'url_list':reverse_lazy('srea:p_asignatura')
    }
    return render(request, 'unidad/unidades.html', context)


@login_required
@permission_required('unidad.add_unidad')
def NewModule(request, asignatura_id):
    user = request.user
    
    course = get_object_or_404(Asignatura, id=asignatura_id)#calculo
    if not request.user.is_staff :
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = UnidadCreateForm(request.POST, request.FILES)
            if form.is_valid():
                nombre=form.cleaned_data.get('nombre')
                descripcion=form.cleaned_data.get('descripcion')
                m = Unidad.objects.create(nombre=nombre,descripcion=descripcion,docente=user)# en docente registramos directamente en launidad
                course.unidad.add(m)# registramos la unidad en la asignatura
                course.save()
                return redirect('srea:primeraU', asignatura_id=asignatura_id)
        else:
            form = UnidadCreateForm()
    context = {
		'form': form,
        'asignatura_id':asignatura_id,
        'url_list':reverse_lazy('srea:p_asignatura')
	}
    return render(request, 'unidad/newmodule.html', context)


@login_required
@permission_required('unidad.change_unidad')
def EditMudule(request, unidad_id, asignatura_id):#Editar unidad
    course = get_object_or_404(Unidad, id=unidad_id)
    #quiz = get_object_or_404(Quizzes, id=quiz_id)
    #print(quiz)
    if request.user.is_staff:
		#return HttpResponseForbidden()
        if request.method == 'POST':
            form = UnidadCreateForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                course.nombre = form.cleaned_data.get('nombre')
                course.descripcion = form.cleaned_data.get('descripcion')
                #course.cuestionario=form.cleaned_data.get('cuestionario')
                #quiz=Quizzes.objects.filter(pk=course.cuestionario)
                #print(quiz, '--Tob--')
                #course.cuestionario.set(quiz_id)
                course.save()
                return redirect('srea:primeraU', asignatura_id=asignatura_id)
        else:
            form = UnidadCreateForm(instance=course)
    context = {
		'form': form,
		'course': course,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'unidad/newmodule.html', context)


class UnidadCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Unidad #Indicar el modelo con el cual se va ha trabajar
    form_class=UnidadCreateForm #Importando el formulario con el que voy a trabajar
    template_name='unidad/unidad_create.html' # Debo indicarle la ubicación de mi plantilla
    permission_required='add_unidad'
    success_url= reverse_lazy('srea:primeraU') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro

   
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
        context['title']='Creación de una unidad' #Puedo enviar variables
        context['modelo']='Unidad'#Nombre de identidad
        #context['url_list']=reverse_lazy('srea:primeraU')#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context

class UnidadUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Unidad #Indicar el modelo con el cual se va ha trabajar
    form_class = UnidadCreateForm #Importando el formulario con el que voy a trabajar
    template_name = 'unidad/unidad_create.html' #Debo indicarle la ubicación de mi plantilla
    permission_required='change_unidad'


    success_url = reverse_lazy('srea:unidad_create') #Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
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
        context['title']='Actualización de una unidad' #Puedo enviar variables
        context['modelo']='Unidad'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:unidad')#Ruta abosluta lista de asignatura
        context['action']='edit'#Enviar variable action
        return context

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


