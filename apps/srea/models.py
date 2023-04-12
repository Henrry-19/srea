from django.db import models
from datetime import datetime
from django.forms import model_to_dict # Librería que permite convertir mi modelo a tipo diccionario
from core.settings import MEDIA_URL, STATIC_URL
from apps.srea.tipo_pregunta import tipo_preguntas
from apps.user.models import User
from apps.quiz.models import *
from datetime import date
import  random
import uuid
#from srea.encryption_util import*

##################Carrera######################
class Carrera(models.Model):
	facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE, related_name="facultad", verbose_name="Facultad")
	nombre = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
	duracion = models.PositiveSmallIntegerField(verbose_name='Duración', default=5)

	###Crear un método llamado toJSON###
	def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
		item=model_to_dict(self) #Mi atributo self contiene mi modelo
		#item['curso']=[{'id':c.id, 'nombre':c.nombre_ciclo}for c  in self.curso.all()]
		return item

	def __str__(self):
		return self.nombre
	

##################Curso######################
class Ciclo(models.Model): ###-->Ciclos-->Categoria
	nombre_ciclo = models.CharField(max_length=150, verbose_name="Nombre de ciclo")   
	carrera=models.ForeignKey(Carrera,on_delete=models.CASCADE, related_name="carrera", verbose_name="Carrera")
	fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
	

	def get_carrera(self):
		if self.carrera:
				name=str(self.carrera.nombre)
				#print(name)
				return name
		return ''
	
	def get_carrera_ciclo(self):
		if self.ciclo:
				name=str(self.ciclo.nombre)
				#print(name)
				return name
		return ''

		###Crear un método llamado toJSON###
	def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
		item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
		item['fecha']=self.fecha.strftime('%Y-%m-%d')
		item['carrera']=self.get_carrera()
		#item['asignatura']=[{'id':c.id, 'nombre':c.nombre}for c  in self.asignatura.all()]
		return item

	def __str__(self):
		return str(self.nombre_ciclo)
	
	class Meta:
		verbose_name = 'Ciclo'
		verbose_name_plural = 'Ciclos'
		ordering = ['id'] 


##################Asignatura######################    
class Asignatura(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	nombre=models.CharField(max_length=150, verbose_name='Nombre', unique=True)
	detalle=models.TextField(verbose_name='Detalle de la asignatura')
	imagen = models.ImageField(upload_to='asignatura/%Y/%m/%d', null=True, blank=True)
	ciclo=models.ForeignKey(Ciclo,on_delete=models.CASCADE, related_name="ciclo", verbose_name="Ciclo")
	docente = models.ForeignKey(User,on_delete=models.CASCADE, related_name='course_owner', verbose_name='Docente')
	users= models.ManyToManyField(User,blank=True,related_name="users", verbose_name="Usuario" )#Matriculados
	unidad= models.ManyToManyField(Unidad,blank=True,related_name="unidad", verbose_name="Unidad" )
  
	def get_image(self):
		if self.imagen:
			return '{}{}'.format(MEDIA_URL, self.imagen)
		return '{}{}'.format(STATIC_URL, 'img/usuario.png')

	def get_curso(self):
		if self.docente:
				name=str(self.docente.get_full_name())
				#print(name)
				return name
		return ''
	#def get_usuarios(self):
	#	users=self.users
	#	users['users'] = [{'id':u.id, 'username':u.username}for u  in self.users.all()]
		#name=str(self.users)
		#print(users)
	#	return users
	#	return ''
			
		#return '{}{}'.format(STATIC_URL, 'img/usuario.png')
		
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
		#item['perfil']=self.get_user_imagen()
		item['users']=[{'id':u.id, 'username':u.username,'groups':u.groups.all, 'firts_name':u.first_name,'last_name':u.last_name, 'imagen':u.imagen}for u  in self.users.all()]
		item['unidad']=[{'id':u.id, 'nombre':u.nombre}for u  in self.unidad.all()]
		#print(item)

		return item

	def __str__(self):
		return self.nombre 

	class Meta:
		verbose_name = 'Asignatura'
		verbose_name_plural = 'Asignaturas'
		ordering = ['id']   

#######################################Completion##########################################################

class Completion(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
	completed = models.DateTimeField(auto_now_add=True)
	quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.user.username