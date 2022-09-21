from distutils.command.upload import upload
from msilib.schema import Class
from pydoc import describe
from pyexpat import model
#from random import random
#import random as random
import random

from statistics import mode
from turtle import up


from django.contrib.auth.models import User

from django.forms import model_to_dict

from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Usuario(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    correo=models.EmailField(unique=True)
    clave=models.CharField(max_length=8)
    fecha_nacimiento=models.DateField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def toJSON(self): #Método para devolver un diccionario de los atributos del modelo
        item= model_to_dict(self, exclude='clave, estado')

        return item
    
class Cuenta(models.Model):
    correo=models.EmailField()
    clave=models.CharField(max_length=8)
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    

class Reporte(models.Model):
    titulo=models.CharField(max_length=100)
    descripcion=models.TextField()
    estado=models.BooleanField(default=True)
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)

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
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
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

#    def __str__(self):
#        if self.foto:
#            return '{}{}'.format(MEDIA_URL, self.foto)
#        return '{}{}'.format(STATIC_URL, 'img/user_png')


class Indicacion(models.Model):
    titulo=models.CharField(max_length=100)
    descripcion=models.TextField()
    tiempo=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo

class Asignatura(models.Model):
    nombre=models.CharField(max_length=50)
    detalle=models.TextField()
    foto=models.ImageField(upload_to="images/")
    estado=models.BooleanField(default=False)
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Nivel(models.Model):
    nombre=models.CharField(max_length=50)
    numero=models.IntegerField()
    descripcion=models.TextField()
    estado=models.BooleanField(default=False)
    user=models.ForeignKey(Asignatura, on_delete=models.CASCADE)

class Test(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=False)
    user=models.ForeignKey(Nivel, on_delete=models.CASCADE)

########Trabajando con las preguntas y respuestas##########

class Pregunta(models.Model):
    NUMER_DE_RESPUESTAS_PERMITIDAS = 1 #Número de respuestas permitidas igual a 1
    texto=models.TextField(verbose_name='Texto de la pregunta')
    max_puntaje=models.DecimalField(verbose_name='Máximo Puntaje', default=3, decimal_places=2,max_digits=6)

    def __str__(self):
        return self.texto



class ElegirRespuesta(models.Model): #ElegirRespuesta, conectada con la respuesta
    MAXIMO_RESPUESTA=4 #Máximo número de respuestas  #opciones #Cuatro campos
    pregunta=models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE) #Pregunta conectada con posible respuesta
    correcta=models.BooleanField(verbose_name='Respuesta correcta', default=False,null= False)
    respuesta=models.TextField(verbose_name='Texto de la respuesta')
    
    def __str__(self):
        return self.respuesta

class Usuario2(models.Model): #QuizUsuario
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Usuario tiene que estar logueado para responder las preguntas
    puntaje_total = models.DecimalField(verbose_name='Puntaje total',default=0,decimal_places=2,max_digits=10)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta,quizUsuario=self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas=PreguntasRespondidas.objects.filter(quizUsuario=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes=Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

    def validar_intento(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id!=respuesta_seleccionada.pregunta_id: 
            return
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada

        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje  
            pregunta_respondida.respuesta = respuesta_seleccionada

        pregunta_respondida.save()

class PreguntasRespondidas(models.Model):
    quizUsuario= models.ForeignKey(Usuario2, on_delete=models.CASCADE, related_name='intentos') #Mandamos al usuario en preguntas respondidas
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(default=False, null=False) 
    puntaje_obtenido = models.DecimalField(default=0, decimal_places=2, max_digits=6)

