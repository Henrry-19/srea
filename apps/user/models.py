from django.contrib.auth.models import AbstractUser
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from crum import get_current_request

from apps.srea.genero import genero_ficha_informacion
from apps.srea.estado_civil import estado_civil_ficha_informacion
from apps.srea.etnia import etnia_ficha
from datetime import datetime
from datetime import date
from  apps.srea.models import Curso

#from apps.srea.models import Matricula
##################FichaUser######################
class Ficha(models.Model):
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=10, choices=genero_ficha_informacion, default='Masculino', verbose_name='Genero')
    direccion=models.CharField(max_length=50, verbose_name='Dirección')
    ocupacion=models.CharField(max_length=50, verbose_name='Ocupación') #Ingresar como lista-clase ocupación
    tecnica_estudio=models.CharField(max_length=50,null=True, verbose_name='Técnica de estudio')
    etnia=models.CharField(choices=etnia_ficha,max_length=10, verbose_name='Etnia')
    estado_civil= models.CharField(choices=estado_civil_ficha_informacion, max_length=10, verbose_name='Estado civil')
    
 ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        return item

    def __str__(self):
        return self.dni #llamar con clave primaria
    
    def calcular_años(self):
        return date.today().year - self.birthday.year
    
    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['id']

##################Indicación######################
class Indicacion(models.Model):
    titulo=models.CharField(max_length=100, verbose_name="Título")
    descripcion=models.TextField(verbose_name='Descripción')
    fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Indicación'
        verbose_name_plural = 'Indicaciones'
        ordering = ['id']

##################User######################
class User(AbstractUser):
    imagen=models.ImageField(upload_to='users/%Y/%m/%d',null=True,blank=True)
    email=models.EmailField(max_length=254,unique=True,verbose_name='Correo Electrónico')
    ficha= models.OneToOneField(Ficha,null=True,blank=True,on_delete=models.SET_NULL,related_name="ficha", verbose_name="Ficha")
    curso = models.ForeignKey(Curso,null=True, blank=True, on_delete=models.SET_NULL,related_name="carrera", verbose_name="Carrera")
    indicacion= models.ForeignKey(Indicacion,null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Indicación" )
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/usuario.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions ', 'last_login']) #Me permite obtener un diccionario a partir del modelo que se le enví
        if self.last_login:
            item['last_login']=self.last_login.strftime('%Y-%m-%d')
        item['date_joined']=self.date_joined.strftime('%Y-%m-%d')
        item['imagen']=self.get_image()
        item['full_name']=self.get_full_name()
        item['groups']=[{'id':g.id, 'name':g.name}for g  in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0] #Seleecionar el primer perfil de usuario
        except:
            pass


