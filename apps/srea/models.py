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

class Catalog(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    active = models.BooleanField(null=True, default=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500) 
    order = models.PositiveSmallIntegerField(null=True)
    createdAt = models.DateTimeField('CreatedAt', auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField('UpdatedAt', auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'catalog'
        verbose_name = 'catalog'
        verbose_name_plural = 'catalogs'
        ordering = ['code', ]

    def __str__(self):
        return self.name


class CatalogItem(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    active = models.BooleanField(null=True, default=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500) 
    order = models.PositiveSmallIntegerField(null=True)
    createdAt = models.DateTimeField('CreatedAt', auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField('UpdatedAt', auto_now=True, auto_now_add=False)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name="catalog_item")

    class Meta:
        db_table = 'catalog_item'
        verbose_name = 'catalog_item'
        verbose_name_plural = 'catalog_items'
        ordering = ['catalog', 'order', 'name']

    def __str__(self):
        return self.name


class Facultad(models.Model):
	nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
	descripcion =models.TextField(verbose_name='Descripción')
	#carrera = models.ManyToManyField(Carrera, blank=True,related_name="carrera", verbose_name="Carreras")

	###Crear un método llamado toJSON###
	def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
		item=model_to_dict(self) #Mi atributo self contiene mi modelo
		#item['carrera']=[{'id':g.id, 'nombre':g.nombre}for g  in self.carrera.all()]
		return item

	def __str__(self):
		return self.nombre


class Unidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=False)
    descripcion =models.TextField(verbose_name='Descripción')
    
	
	
    def __str__(self):
	    return self.nombre

################################QUIZ-UNIDAD#########################################
class UnidadQuiz(models.Model):
	quiz=models.ForeignKey(Quiz, related_name="quiz_unidad",verbose_name=("Registrar quiz"), on_delete=models.CASCADE)
	unidad=models.ForeignKey(Unidad, related_name="unidad_quiz",verbose_name=("Registrar unidad"), on_delete=models.CASCADE)



	def __str__(self):
	    return self.quiz.name

################################QUIZ-USUARIO#########################################
class UserQuiz(models.Model):
	quiz=models.ForeignKey(Quiz, related_name="quiz_users",verbose_name=("Registrar quiz"), on_delete=models.CASCADE)
	users=models.ManyToManyField(User,blank=True, related_name="users_quiz",verbose_name=("Registrar usuario"))



	def __str__(self):
	    return self.quiz.name

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
	users= models.ManyToManyField(User,blank=True,related_name="users", verbose_name="Usuario" )#Matriculados
	unidad= models.ManyToManyField(Unidad,blank=True,related_name="unidad_asignatura", verbose_name="Unidad" )
  
	def get_image(self):
		if self.imagen:
			return '{}{}'.format(MEDIA_URL, self.imagen)
		return '{}{}'.format(STATIC_URL, 'img/usuario.png')

	def get_curso(self):
		if self.users.all():
			for u in self.users.all():
				for g in u.groups.all():
					if g.name=="Docente":
						name=str(u.get_full_name())
						#print("-->",name)
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

##############################################

class MensajenAsignatura(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	asignatura= models.ForeignKey(Asignatura,blank=True,on_delete=models.CASCADE,related_name="asignatura", verbose_name="Asignatura")
	titulo=models.CharField(max_length=100, verbose_name="Título del mensaje")
	descripcion=models.TextField(max_length=900,blank=True, null=True,verbose_name='Descripción del mensaje')
	fecha=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación del mensaje")
	#user_indicacion=models.ManyToManyField(User,blank=True,related_name="user_ind", verbose_name="Indicación de usuarios" )
	
	def __str__(self):
		return self.titulo
	
	class Meta:
		verbose_name = 'Mensaje'
		verbose_name_plural = 'Mensajes'
		ordering = ['id']

	

class FileUploaded(models.Model):
    nombre=models.CharField(max_length=100, verbose_name="Nombre del archivo")
    file = models.FileField(upload_to='archivo/%Y/%m/%d', null= True, blank= True, verbose_name="Cargar archivo")#donde se va a subir
    observation = models.CharField(max_length=200, null=True, verbose_name='Observación')

    def __str__(self):
        return self.observation

    class Meta:
        db_table = 'file_uploaded'
        verbose_name = 'file_uploaded'
        verbose_name_plural = 'file_uploadeds'
        ordering = ['id']



class SubirArchivos(models.Model):
    nombre=models.CharField(max_length=100, verbose_name="Nombre del archivo")
    archivo = models.FileField(upload_to='formato/%Y/%m/%d', null= True, blank= True, verbose_name="Cargar archivo")#donde se va a subir
    observación = models.CharField(max_length=200, null=True, verbose_name='Observación')

    def __str__(self):
        return self.observación
    

    class Meta:
        verbose_name = 'subir_archivo'
        verbose_name_plural = 'subir_archivos'
        ordering = ['id']





@receiver(pre_save, sender=FileUploaded)
def archivo_cargado_pre_save(sender, instance, **kwargs):
    from apps.quiz.layers.application.service_app_uploaded_archive import ArchivoCargadoAppService
    
    ArchivoCargadoAppService.pre_procesar_datos()

#from django.shortcuts import render, redirect, get_object_or_404

@receiver(post_save, sender=FileUploaded)
def archivo_cargado_post_save(sender, instance, created, **kwargs):
    #from apps.srea.models import Unidad #--->Solución para la importación circular
    from apps.quiz.layers.application.service_app_uploaded_archive import ArchivoCargadoAppService
    ArchivoCargadoAppService.procesar_datos(instance)##