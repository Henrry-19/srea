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

#from apps.srea.models import Asignatura
##################FichaUser######################
##################User######################
class User(AbstractUser):
    imagen=models.ImageField(upload_to='users/%Y/%m/%d',null=True,blank=True)
    email=models.EmailField(max_length=254,unique=True,verbose_name='Correo Electrónico')
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/usuario.png')

#    def get_curso(self):
#        if self.curso:
#            name=str(self.curso)
#            return name
#        return ''
        
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions ', 'last_login']) #Me permite obtener un diccionario a partir del modelo que se le enví
        if self.last_login:
            item['last_login']=self.last_login.strftime('%Y-%m-%d')
        item['date_joined']=self.date_joined.strftime('%Y-%m-%d')
        item['imagen']=self.get_image()
        item['full_name']=self.get_full_name()
#        item['curso']=self.get_curso()
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


class Ficha(models.Model):
    user= models.OneToOneField(User,blank=True,on_delete=models.CASCADE,related_name="userF", verbose_name="Usuario")
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=10, choices=genero_ficha_informacion, default='Masculino', verbose_name='Genero')
    direccion=models.CharField(max_length=50, verbose_name='Dirección')
    ocupacion=models.CharField(max_length=50, verbose_name='Ocupación') #Ingresar como lista-clase ocupación
    tecnica_estudio=models.CharField(max_length=50,null=True, verbose_name='Técnica de estudio')
    etnia=models.CharField(choices=etnia_ficha,max_length=10, verbose_name='Etnia')
    estado_civil= models.CharField(choices=estado_civil_ficha_informacion, max_length=10, verbose_name='Estado civil')
    


    
    def calcular_años(self):
        return date.today().year - self.birthday.year

    def get_user(self):
        if self.user:
            name=str(self.user.get_full_name())
            return name
        return ''
 ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        item['user']=self.get_user()
        return item

    def __str__(self):
        return self.dni #llamar con clave primaria


    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['id']

##################Indicación######################
class Indicacion(models.Model):
    users= models.ManyToManyField(User,blank=True,related_name="user", verbose_name="Usuario" )
    titulo=models.CharField(max_length=100, verbose_name="Título")
    descripcion=models.TextField(verbose_name='Descripción')
    fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Indicación'
        verbose_name_plural = 'Indicaciones'
        ordering = ['id']
