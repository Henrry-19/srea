from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.http import *
from django.urls import reverse_lazy
from apps.srea.mixins import*
from apps.srea.forms import*
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.srea.encryption_util import*


class FileListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,View):
    model= SubirArchivos
    template_name = 'file/file_lista.html'
    permission_required='view_fileuploaded'
    def get(self,request, *args, **kwargs):
        #user=request.user
        if request.user.is_staff : 
            file = SubirArchivos.objects.all()
        if  not request.user.is_staff:
            file = SubirArchivos.objects.all()

        context={
            'file':file,
            #'url_create':reverse_lazy('quiz:archivo_cargado_crear2'),
            #'list_url':reverse_lazy('srea:p_asignatura'),
            'title':'Lista de Archivos',
            'modelo':'File',
            'date_now':datetime.now()  
        }

        return render(request, 'file/file_lista.html', context)
    
    def get_context_data(self, **kwargs): #Método que devuelve un diccionario que representa el contexto de la plantilla
        context = super().get_context_data(**kwargs) #Obtengo el diccionario que devuelve el método
        context['title']='Lista de archivos' #Puedo enviar variables
        context['url_create']=reverse_lazy('srea:asignatura')#Ruta abosluta creación de usuario
        context['url_list']=reverse_lazy('srea:p_asignatura')#Ruta abosluta lista de usuario
        context['modelo']='Files'#Nombre de identidad
        return context