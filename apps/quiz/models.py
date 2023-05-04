from django.db import models

from datetime import datetime
from django.forms import model_to_dict # Librería que permite convertir mi modelo a tipo diccionario
from core.settings import MEDIA_URL, STATIC_URL
from apps.user.models import User
#from django.contrib.auth.models import User
from ckeditor.fields import RichTextField ###Aquí está####
import  random
from apps.srea.encryption_util import*
from cryptography.fernet import Fernet
#import datetime
##################Facultad######################
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
##################Respuesta######################


################################Borrador--Modelos##########################################################3
class Respuesta(models.Model):
    #pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="pregunta_respuesta")
    respuesta=models.TextField(verbose_name='Texto de la respuesta')
    correcta = models.BooleanField(default=False)


    def __str__(self):
        return self.respuesta

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['id']
##################Pregunta######################
class Pregunta(models.Model):
    respuesta=models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name="pregunta_respuesta")
    texto=models.TextField(null=True, blank=True,verbose_name='Texto de la pregunta')
    
    
    def get_respuesta(self):
        respuesta_objs=list(Respuesta.objects.filter(pregunta = self))
        random.shuffle(respuesta_objs)
        data = []
        for respuesta_obj  in respuesta_objs:
            data.append({
                'respuesta':respuesta_obj.respuesta
            })
        return data

    def get_respuestas(self):
        respuesta=list(self.pregunta_respuesta.all())
        random.shuffle(respuesta)
        return respuesta

    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        #item['respuesta']= self.get_respuesta()
        return item

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['id']
##################Quiz######################
class Cuestionario(models.Model):
    #unidad = models.ManyToManyField(Unidad,blank=True,related_name="unidades", verbose_name="Unidad")
    titulo = models.CharField(max_length=150, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True,verbose_name="Descripción")
    numero_preguntas=models.IntegerField(verbose_name="Numero de preguntas")
    tiempo=models.IntegerField(verbose_name="Duración del Test")
    required_score_to_pass = models.IntegerField(verbose_name="Puntaje requerido")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación") 
    pregunta=models.ManyToManyField(Pregunta,blank=True, related_name="preguntas", verbose_name="Pregunta")
    facultades=models.ManyToManyField(Facultad,blank=True, related_name="facultades", verbose_name="Facultades")
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        item['unidad']=[{'id':u.id, 'nombre':u.nombre}for u  in self.unidad.all()]
        item['fecha']=self.fecha.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        return self.titulo

    def get_pregunta(self):
        #return self.pregunta_set.all()[:self.numero_preguntas]
        pregunta_objs=list(Pregunta.objects.filter(test=self.numero_preguntas))
        random.shuffle(pregunta_objs)
        data = []
        for pregunta_obj  in pregunta_objs:
            data.append({
                'pregunta':pregunta_obj.texto
            })
        return data

    def get_preguntas(self):
        #return Test.pregunta_set.all()
        preguntas=list(self.test.all())
        random.shuffle(preguntas)
        return preguntas[:self.numero_preguntas]

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['id']
##################Perfil--Resultado######################
class Resultado(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE, verbose_name="Cuestionario")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    score = models.FloatField(verbose_name="Puntaje")
    
    def __str__(self):
        return str(self.pk)
    


#####################################Nuevos--Modelos#####################################################
##############################PARA EL TEST##################################

class Categoria(models.Model):
    nombre_cat = models.CharField(max_length=900)
    
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
		#item['asignatura']=[{'id':c.id, 'nombre':c.nombre}for c  in self.asignatura.all()]
        return item
    
    def __str__(self):
        return self.nombre_cat
    

    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class ItemCat(models.Model):
    cat=models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    nombreItem = models.CharField(max_length=900)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['id']


class Answer(models.Model):##--> Respuesta
    answer_text=models.CharField(max_length=900, verbose_name='Texto de la respuesta')
    respuesta = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.answer_text
    
class Question(models.Model):##--> Pregunta
    question_text = models.CharField(max_length=900, verbose_name='Texto de la pregunta')
    answers = models.ManyToManyField(Answer, verbose_name='Respuestas') #Respuesta


    def __str__(self):
        return self.question_text
    

class Quizzes(models.Model):#Cuestionarios
    cat=models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    title = models.CharField(max_length=200, verbose_name="Título", unique=True)
    description = RichTextField(verbose_name="Descripción")
    date = models.DateTimeField(auto_now_add=True) # Fecha de creación del cuestionario
    due = models.DateField(default=datetime.now,verbose_name='Fecha de vencimiento') # Fecha de realización del cuestionario
    allowed_attemps = models.PositiveIntegerField(verbose_name='Número de intentos') # Veces que se permite a la persona dar el test
    time_limit_mins = models.PositiveIntegerField(verbose_name='Tiempo límite') # Límite de tiempo
    questions = models.ManyToManyField(Question) # Preguntas

    def __str__(self):
        return self.title
    
    def fecha(self):
        due=self.due.strftime('%Y-%m-%d')
        return due

    def toJSON(self):
        item = model_to_dict(self)
        item['due'] = self.due.strftime('%Y-%m-%d')
        return item

    class Meta:
        #permissions = (("view_quizzes","add_quizzes"))
        verbose_name = 'Quizze'
        verbose_name_plural = 'Quizzes'
    
class Attempter(models.Model): #IntentosResultado--->Resultado:Guardo mis intentos
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    quiz= models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completed = models.DateTimeField(auto_now_add=True)#Fecha


    def __str__(self):
        return self.quiz.title
    
class Attempt(models.Model): #Intento--Enviar--->Contestar
    #quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    attempter = models.ForeignKey(Attempter, on_delete=models.CASCADE)#Mis intentos
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)#Respuestas

    def __str__(self):
        #return self.attempter.user.username + ' - ' + self.answer.answer_text
        return self.answer.answer_text
    

##################Unidad####################
class Unidad(models.Model):
    #docente=models.ForeignKey(User, on_delete=models.CASCADE, related_name='unidad_docente', verbose_name='Docente')
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=False)
    descripcion =models.TextField(verbose_name='Descripción')
    cuestionario=models.ManyToManyField(Quizzes, blank=True, related_name="cuestionarios", verbose_name="Cuestionario")
    #asignaturas=models.ManyToManyField(Asignatura, blank=True, related_name="asignaturas", verbose_name="Asignatura")

    def get_test(self):
        test_objs=list(Cuestionario.objects.filter(unidad=self))
        data = []
        for u_obj  in test_objs:
            print(u_obj)
            data.append(u_obj)
        return data
    def get_docente(self):
        if self.docente:
            nombre=str(self.docente)
            return nombre
        return ''

    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        #item['test']=[{'id':t.id, 'titulo':t.titulo}for t  in self.get_test()]
        item['cuestionario']=[{'id':c.id, 'titulo':c.titulo}for c  in self.cuestionario.all()]
        item['docente']=self.get_docente()
        return item

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['id']


