from django.contrib.auth.models import AbstractUser
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from crum import get_current_request
from datetime import datetime
from datetime import date
import uuid
####################################################
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
#####################CHOICES#########################
from apps.user.vistas.choices.nacionalidad import nacionalidad_pais
from apps.user.vistas.choices.tecnicas_estudio import tecnicas_de_estudio
from apps.user.vistas.choices.ocupaciones import ocupaciones_de_usuarios


from apps.srea.etnia import etnia_ficha
from apps.srea.estado_civil import estado_civil_ficha_informacion
from apps.srea.genero import genero_ficha_informacion
####################################################

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
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user= models.OneToOneField(User,blank=True,on_delete=models.CASCADE,related_name="userF", verbose_name="Usuario")
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=10, choices=genero_ficha_informacion, default='Masculino', verbose_name='Genero')
    direccion=models.CharField(max_length=50, verbose_name='Dirección')
    ocupacion=models.CharField(choices=ocupaciones_de_usuarios,max_length=200, verbose_name='Ocupación') #Ingresar como lista-clase ocupación
    tecnica_estudio=models.CharField(choices=tecnicas_de_estudio,max_length=100,null=True, verbose_name='Técnica de estudio')
    etnia=models.CharField(choices=etnia_ficha,max_length=100, verbose_name='Etnia')
    nacionalidad=models.CharField(choices=nacionalidad_pais,max_length=100, verbose_name='Nacionalidad')
    estado_civil= models.CharField(choices=estado_civil_ficha_informacion, max_length=100, verbose_name='Estado civil')
    

    def get_image(self):
        if self.user:
           #return '{}{}'.format(MEDIA_URL, self.user.imagen) 
           print(self.user)
        #return '{}{}'.format(STATIC_URL, 'img/usuario.png')
            
    
    def calcular_años(self):
        return date.today().year - self.birthday.year

    def get_user(self):
        if self.user:
            name=str(self.user.get_full_name())
            return name
        return ''
    
    def get_uuid(self):
        if self.uuid:
            name=str(self.uuid)
            return name
        return ''

    def get_email(self):
        if self.user:
            email=str(self.user.email)
            return email
        return ''
 ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        item['user']=self.get_user()
        item['uuid']=self.get_uuid()
        item['get_image']=self.get_image()
        #item['user']=self.get_quiz()
        return item

    def __str__(self):
        return self.dni #llamar con clave primaria


    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['id']

##################Indicación######################
class Indicacion(models.Model):
    titulo=models.CharField(max_length=100, verbose_name="Título", blank=True, null=True)
    descripcion=models.TextField(max_length=500,blank=True, null=True,verbose_name='Descripción')
    fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    documento = models.FileField(upload_to="pdf/%Y/%m/%d", blank=True, null=True, verbose_name="Subir documento")
    user_indicacion=models.ManyToManyField(User,blank=True,related_name="user_ind", verbose_name="Indicacion de usuarios" )
    ###Podemos tener un campo para cargar el manual de usuario

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Indicacion'
        verbose_name_plural = 'Indicaciones'
        ordering = ['id']

