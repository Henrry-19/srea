from django.db import models
from datetime import datetime
from django.forms import model_to_dict # Librería que permite convertir mi modelo a tipo diccionario
from core.settings import MEDIA_URL, STATIC_URL
from apps.srea.tipo_pregunta import tipo_preguntas
#from apps.user.models import*
from datetime import date
#from  apps.user.models import Carrera
import  random

##################Carrera######################
class Facultad(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    descripcion =models.TextField(verbose_name='Descripción')

    ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        return item

    def __str__(self):
        return self.nombre
##################Asignatura######################    
class Asignatura(models.Model):
    nombre=models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    detalle=models.TextField(verbose_name='Detalle de la asignatura')
    imagen = models.ImageField(upload_to='asignatura/%Y/%m/%d', null=True, blank=True)
  
    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/usuario.png')
    
     ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item = model_to_dict(self, exclude=['usuario'])
        item['imagen']=self.get_image()
        return item

    def __str__(self):
        return self.nombre 

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['id']   

##################Curso######################
class Curso(models.Model):
    nombre_ciclo = models.CharField(max_length=150, verbose_name="Nombre de ciclo")   
    asignatura=models.ManyToManyField(Asignatura,blank=True, related_name="asignatura", verbose_name="Asignatura")
    fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

        ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        item['fecha']=self.fecha.strftime('%Y-%m-%d')
        item['asignatura']=[{'id':c.id, 'name':c.nombre}for c  in self.asignatura.all()]
        return item

    def __str__(self):
        return str(self.nombre_ciclo)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id']  

        
##################Carrera######################
class Carrera(models.Model):
    facultad = models.ForeignKey(Facultad,null=True, blank=True, on_delete=models.CASCADE,related_name="facultad", verbose_name="Facultad")
    curso = models.ManyToManyField(Curso, blank=True,related_name="curso", verbose_name="Curso")
    nombre = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    duracion = models.PositiveSmallIntegerField(verbose_name='Duración', default=5)

    ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        item['curso']=[{'id':c.id, 'nombre':c.nombre_ciclo}for c  in self.curso.all()]
        return item

    def __str__(self):
        return self.nombre

##################Test######################

class Test(models.Model):
    asignatura = models.ForeignKey(Asignatura,on_delete=models.CASCADE, verbose_name="Asignatura")
    titulo = models.CharField(max_length=150, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True,verbose_name="Descripción")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación") 
    
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        item['fecha']=self.fecha.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['id']
   
##################Pregunta######################

class Pregunta(models.Model):
    test=models.ForeignKey(Test, on_delete=models.CASCADE, related_name="test")
    pregunta=models.TextField(null=True, blank=True,verbose_name='Texto de la pregunta')
    tipoPregunta= models.CharField(max_length = 2, choices=tipo_preguntas, verbose_name='Tipo de preguntas')
    
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        return item

    def __str__(self):
        return self.pregunta

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['id']

    def get_respuestas(self):
        respuesta_objs=list(Respuesta.objects.filter(pregunta = self))
        random.shuffle(respuesta_objs)
        data = []
        for respuesta_obj  in respuesta_objs:
            data.append({
                'respuesta':respuesta_obj.respuesta
            })
        return data
##################Respuesta######################

class Respuesta(models.Model):
    pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="pregunta_respuesta")
    respuesta=models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.respuesta

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['id']







