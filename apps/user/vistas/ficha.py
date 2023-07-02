from typing import Any, Optional
from django.db import models
from django.views.generic import* #importando la vista genérica
from apps.user.models import* #importando los modelos
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator #importando el método decorador
from django.http import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.srea.mixins import*
from apps.user.forms import*

###########PARA PDF#############################
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



class FichaListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView): #Primera vista basada en clase ListView, permite sobrescribir métodos
    model= Ficha#Primero se indica el modelo o entidad
    template_name = '../templates/ficha/ficha_lista.html' #Indicarle cual es la plantilla
    permission_required='view_ficha'
    
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
                if request.user.is_staff :
                    for i in Ficha.objects.all():
                        item= i.toJSON()
                        item['position']=position
                        data.append(item)#Incrusto cada uno de mis elementos dentro de mi array
                        position+=1
                if  not request.user.is_staff:
                    user=User.objects.filter(pk=request.user.pk)
                    for u in user:
                    #   if u.ficha!=None:
                        for i in Ficha.objects.filter(user=u.id):
                            item= i.toJSON()
                            item['position']=position
                            data.append(item)#Incrusto cada uno de mis elemntos dentro de mi array
                            position+=1  
                        
            else:
                data["error"]='Ha ocurrido un error'
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Listado de Fichas' #Puedo enviar variables
        #context['url_create_login']=reverse_lazy('user:user_login')#Ruta abosluta creación de usuario
        context['url_create']=reverse_lazy('user:ficha')#Ruta abosluta creación de usuario
        context['url_list']=reverse_lazy('user:ficha_list')#Ruta abosluta lista de usuario
        context['date_now']=datetime.now() #Se obtiene la fecha de hoy
        context['modelo']='Ficha'#Nombre de identidad  'date_now':datetime.now()  
        return context

class FichaCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=Ficha #Indicar el modelo con el cual se va ha trabajar

    form_class=FichaCreateForm#Importando el formulario con el que voy a trabajar
    template_name='ficha/ficha_create.html' # Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('user:ficha') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro
    permission_required='add_ficha'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
   
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

   
    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        #form = FichaCreateForm(request.FILES, request=request)
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            action= request.POST['action'] #Recupero la variable action en mi método POST, cada vez que se haga una petición
            
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
        context['title']='Creación de un ficha' #Puedo enviar variables
        context['modelo']='Ficha'#Nombre de identidad
        context['url_list']=reverse_lazy('user:ficha_list')#Ruta abosluta lista de usuario
        context['action']='add'#Enviar variable action
        return context


class FichaUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Ficha #Indicar el modelo con el cual se va ha trabajar
    form_class = FichaCreateForm #Importando el formulario con el que voy a trabajar
    template_name = 'ficha/ficha_create.html' #Debo indicarle la ubicación de mi plantilla
    success_url = reverse_lazy('user:ficha_list') #Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    #@method_decorator(csrf_exempt) #Mecanismo de defensa de django
    permission_required='change_ficha'
    def dispatch(self, request, *args, **kwargs):
        #self.object = self.get_object()#Le decimos que la clase object va a hacer igual a lo que tenemos en lainstancia de nuestro objeto, para que el funcionamiento no se altere
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return Ficha.objects.get(uuid=self.kwargs.get("uuid"))

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
        context['title']='Actualización de una ficha' #Puedo enviar variables
        context['modelo']='Ficha'#Nombre de identidad
        context['url_list']=self.success_url#Ruta abosluta lista de asignatura
        context['action']='edit'#Enviar variable action
        return context


class FichaUsuarioView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Ficha #Indicar el modelo con el cual se va ha trabajar
    form_class = EditarFichaCreateForm #Importando el formulario con el que voy a trabajar
    template_name = 'ficha/ficha_create.html' #Debo indicarle la ubicación de mi plantilla
    success_url = reverse_lazy('user:ficha_list') #Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    #@method_decorator(csrf_exempt) #Mecanismo de defensa de django
    permission_required='change_ficha'
    def dispatch(self, request, *args, **kwargs):
        #self.object = self.get_object()#Le decimos que la clase object va a hacer igual a lo que tenemos en lainstancia de nuestro objeto, para que el funcionamiento no se altere
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return Ficha.objects.get(uuid=self.kwargs.get("uuid"))
    

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
        context['title']='Actualización de una ficha' #Puedo enviar variables
        context['modelo']='Ficha'#Nombre de identidad
        context['url_list']=self.success_url#Ruta abosluta lista de asignatura
        context['action']='edit'#Enviar variable action
        return context


class FichaDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Ficha #Indicar el modelo con el cual se va ha trabajar
    template_name = 'ficha/ficha_delete.html' #Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('user:ficha_list')#Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    permission_required='delete_ficha'
   
    def dispatch(self, request, *args, **kwargs):
        #self.object = self.get_object() #Le decimos que la clase object va a hacer igual a lo que tenemos en lainstancia de nuestro objeto, para que el funcionamiento no se altere
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return Ficha.objects.get(uuid=self.kwargs.get("uuid"))

    def post(self, request, *args, **kwargs):
        data = {} #Creación de variable tipo diccionario
        try:
            self.object.delete()#La variabe self.object contiene la variable de mi objeto y puedo acceder a los métodos
        except Exception as e:
            data['error'] = str(e) # Si llega a ocurrir un error de la excepion se debe guaradar en la viable e
        return JsonResponse(data) #Retorno como respuesta un JsonResponse
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una ficha'
        context['modelo'] = 'Ficha'
        context['url_list'] = self.success_url
        return context


class FichaPdfView(LoginRequiredMixin,ValidatePermissionRequiredMixin,View):
    permission_required='view_ficha'
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path
    
    def get(self, request, *args, **kwargs):
    # find the template and render it.
        try:
            template = get_template('ficha/ficha_pdf.html')
            ficha=Ficha.objects.get(uuid=self.kwargs['uuid'])
            #if ficha:
            quiz=[]
            for q in ficha.user.user_response.all():
                quiz.append(q.quiz)

            numeros_unicos = list(set(quiz))
           
            prueba_usuario=UserResponse.objects.filter(user=ficha.user.id)
            #else:
            if prueba_usuario:
                respuestas = []
                for p_u in prueba_usuario:
                    respuestas.append(p_u.answer.learning_style)
                #print(respuestas)
                recuentos = defaultdict(int)
                for categoria in respuestas:
                        recuentos[categoria] += 1
                        cat=[]
                        contador=[]
                for categoria, count in recuentos.items():
                            #print(f'{categoria}: {count}')
                        cat.append(categoria.name)
                        contador.append(count)

                if 'N/a' in cat:
                    posicion=cat.index("N/a")
                    cat.remove("N/a")
                    contador.pop(posicion)

                estilo_dominate_usuario=""
                if contador:
                    estilo_dominante = max(contador, key=int)
                    #print("---->",estilo_dominante)
                    posicion_ed=contador.index(estilo_dominante)

                    estilo_dominate_usuario=cat[posicion_ed]
            else:
                vacio = []
                estilo_dominate_usuario="Debe dar examen"


            #for q in sale.user.user_response.all %}
             #   {{q.get_quiz}}
            # endfor 
            #print(UserResponse.objects.filter(user=ficha.user.id))
            context = {
                'sale': Ficha.objects.get(uuid=self.kwargs['uuid']),
                'comp': {'name': 'FICHA DE INFORMACIÓN'},
                'numeros_unicos':numeros_unicos,
                'estilo_dominate_usuario':estilo_dominate_usuario,
                'fecha_impresion':datetime.now()
                }
            html=template.render(context)

        # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'   
        # create a pdf

            pisa_status = pisa.CreatePDF(
                html, dest=response )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('user:ficha_list'))