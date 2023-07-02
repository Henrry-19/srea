from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.srea.models import *
from apps.srea.mixins import*
from django.views.generic import* #importando la vista genérica
from collections import defaultdict
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.srea.forms import*
from django.http import *
############################################################################
class CatalogItemListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,View):
    model= CatalogItem
    template_name = 'catalogo_item/catalogo_item.html'
    permission_required='view_catalogitem'
    def get(self,request, *args, **kwargs):
        #user=request.user
        if request.user.is_staff : 
            cat_item = CatalogItem.objects.all()
        if  not request.user.is_staff:
            cat_item = CatalogItem.objects.all()
        #print(catalogo_item)
        context={
            'cat_item':cat_item,
            'url_create':reverse_lazy('srea:catalogo_item_create'),
            'list_url':reverse_lazy('srea:catalogo_item'),
            'title':'Lista de ítems',
            'modelo':'Ítems del Catálogo',
            'date_now':datetime.now()  
        }

        return render(request, 'catalogo_item/catalogo_item.html', context)
    
    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        return context

class CatalogoItemCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model=CatalogItem #Indicar el modelo con el cual se va ha trabajar
    form_class=CatalogoItemCreateForm #Importando el formulario con el que voy a trabajar
    template_name='catalogo_item/catalogoItem_create.html' # Debo indicarle la ubicación de mi plantilla
    #success_url= reverse_lazy('srea:catalogo') #Me permite direccionar a otra plantilla, la funnción reverse_lazy me recibe una url como parámetro
    permission_required='add_catalogitem'
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
        context['title']='Creación de Ítems del Catálogo' #Puedo enviar variables
        context['modelo']='Ítems del Catálogo'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:catalogo_item')#Ruta abosluta lista de asignatura
        context['action']='add'#Enviar variable action
        return context
    
class CatalogoItemUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = CatalogItem #Indicar el modelo con el cual se va ha trabajar
    form_class = CatalogoItemCreateForm #Importando el formulario con el que voy a trabajar
    template_name = 'catalogo_item/catalogoItem_create.html' #Debo indicarle la ubicación de mi plantilla
    permission_required='change_catalogitem'
    #success_url = reverse_lazy('srea:catalogo') #Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
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
        context['title']='Actualización de un ítem del Catálogo' #Puedo enviar variables
        context['modelo']='CatálogoItem'#Nombre de identidad
        context['url_list']=reverse_lazy('srea:catalogo_item')#Ruta abosluta lista de asignatura
        context['action']='edit'#Enviar variable action
        return context
    
class CatalogoItemDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = CatalogItem #Indicar el modelo con el cual se va ha trabajar
    template_name = 'catalogo_item/catalogo_item_delete.html' #Debo indicarle la ubicación de mi plantilla
    success_url= reverse_lazy('srea:catalogo_item')#Me permite direccionar a otra plantilla, la función reverse_lazy me recibe una url como parámetro
    permission_required='delete_catalogitem'
 
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
        context['title'] = 'Eliminación de un item de catálogo'
        context['modelo'] = 'Item de Catálogo'
        context['url_list'] = reverse_lazy('srea:catalogo_item')
        return context

