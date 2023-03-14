from django.db import models
from datetime import datetime
from django.forms import model_to_dict # Librería que permite convertir mi modelo a tipo diccionario
from core.settings import MEDIA_URL, STATIC_URL
from apps.srea.tipo_pregunta import tipo_preguntas
from apps.user.models import User
from datetime import date
import  random


##################Asignatura######################    
class Asignatura(models.Model):
	nombre=models.CharField(max_length=150, verbose_name='Nombre', unique=True)
	detalle=models.TextField(verbose_name='Detalle de la asignatura')
	imagen = models.ImageField(upload_to='asignatura/%Y/%m/%d', null=True, blank=True)
	users= models.ManyToManyField(User,blank=True,related_name="users", verbose_name="Usuario" )
  
	def get_image(self):
		if self.imagen:
			return '{}{}'.format(MEDIA_URL, self.imagen)
		return '{}{}'.format(STATIC_URL, 'img/usuario.png')


#    def get_unidad(self):
#        unidad_objs=list(Unidad.objects.filter(asignaturas=self))
#        data = []
#        for u_obj  in unidad_objs:
#            data.append(u_obj)
#        return data
	
	 ###Crear un método llamado toJSON###
	def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
		item = model_to_dict(self, exclude=['usuario'])
		item['imagen']=self.get_image()
		item['users']=[{'id':u.id, 'username':u.username}for u  in self.users.all()]
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
	curso = models.ManyToManyField(Curso, blank=True, related_name="ciclo", verbose_name="Ciclos")
	nombre = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
	duracion = models.PositiveSmallIntegerField(verbose_name='Duración', default=5)

	###Crear un método llamado toJSON###
	def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
		item=model_to_dict(self) #Mi atributo self contiene mi modelo
		item['curso']=[{'id':c.id, 'nombre':c.nombre_ciclo}for c  in self.curso.all()]
		return item

	def __str__(self):
		return self.nombre
##################Carrera######################
class Facultad(models.Model):
	nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
	descripcion =models.TextField(verbose_name='Descripción')
	carrera = models.ManyToManyField(Carrera, blank=True,related_name="carrera", verbose_name="Carreras")

	###Crear un método llamado toJSON###
	def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
		item=model_to_dict(self) #Mi atributo self contiene mi modelo
		item['carrera']=[{'id':g.id, 'nombre':g.nombre}for g  in self.carrera.all()]
		return item

	def __str__(self):
		return self.nombre


