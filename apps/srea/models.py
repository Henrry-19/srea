from distutils.command.upload import upload
from email.policy import default
from enum import unique
from msilib.schema import Class
from pydoc import describe
from pyexpat import model
import random

from statistics import mode
from turtle import up
from unittest.util import _MAX_LENGTH


from django.contrib.auth.models import User

from django.forms import model_to_dict

from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombres, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            nombres = nombres
        )
        usuario.set_password(password)
        usuario.save()
        return usuario
    def create_superuser(self, username, email, nombres, password):
        usuario = self.create_user(
            email,
            username=username,
            nombres = nombres,
            password=password

        )
        usuario.usuario_administrador= True
        usuario.save()
        return usuario


class Usuario(AbstractUser):
    username=models.CharField('Nombre de usuario', unique=True, max_length=100)
    email=models.EmailField('Correo Electrónico',max_length=254,unique=True)
    nombres=models.CharField('Nombres',max_length=200, blank=True, null=True)
    apellidos=models.CharField('Apellidos',max_length=200, blank=True, null=True)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/',max_length=200, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador=models.BooleanField(default=False)
    object = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres']

    def __str__(self): 
        return f'{self.nombres},{self.apellidos}'
    
    def has_perm(self, perm, obj= None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador

class Cuenta(models.Model):
    correo=models.EmailField()
    clave=models.CharField(max_length=8)
    

class Reporte(models.Model):
    titulo=models.CharField(max_length=100)
    descripcion=models.TextField()
    estado=models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

genero_ficha_informacion = (
    ('M', 'Femenino'),
    ('F', 'Masculino')
)

etnia_ficha={
    ('A', 'Afroecuatoriano'),
    ('B', 'Blanco'),
    ('C', 'Cholo'),
    ('I', 'Indigena'),
    ('Mo', 'Montubio'),
    ('Mu', 'Mulato'),
    ('Me', 'Mestizo'),
    ('N', 'Negro'),
    ('O', 'Otro')
}

estado_civil_ficha_informacion=(
    ('S','Soltero/a'),
    ('C','Casado/a'),
    ('D','Divorciado/a'),
    ('V','Viudo/a')
)
class FichaInformacion(models.Model):
    cedula=models.CharField(max_length=10)
    foto = models.ImageField(upload_to='cars',null=True, blank=True)
    edad=models.IntegerField()
    direccion=models.CharField(max_length=50)
    ocupacion=models.CharField(max_length=1) #Ingresar como lista-clase ocupación
    tecnica_estudio=models.CharField(max_length=50,null=True)
    genero=models.CharField(choices=genero_ficha_informacion, max_length=1)
    etnia=models.CharField(choices=etnia_ficha,max_length=2)
    estado_civil= models.CharField(choices=estado_civil_ficha_informacion, max_length=1)
    

    def __str__(self):
        return self.cedula


    def toJSON(self): #Método para devolver un diccionario de los atributos del modelo
        item= model_to_dict(self, exclude='edad,foto')

        return item

#    def __str__(self):
#        if self.foto:
#            return '{}{}'.format(MEDIA_URL, self.foto)
#        return '{}{}'.format(STATIC_URL, 'img/user_png')


class Indicacion(models.Model):
    titulo=models.CharField(max_length=100)
    descripcion=models.TextField()
    tiempo=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.titulo

class Asignatura(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField()
    foto=models.ImageField(upload_to="images/")
    estado=models.BooleanField(default=False)
    

    def toJSON(self): #Método para devolver un diccionario de los atributos del modelo
        item = model_to_dict(self, exclude='foto,estado')
        return item

    


class Nivel(models.Model):
    nombre=models.CharField(max_length=50)
    numero=models.IntegerField()
    descripcion=models.TextField()
    estado=models.BooleanField(default=False)
   

class Test(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=False)
   

##################

class Pregunta(models.Model):
    texto=models.TextField(verbose_name='Texto de la pregunta')
    

    def __str__(self):
        return self.texto






