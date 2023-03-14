from django.db import models

from datetime import datetime
from django.forms import model_to_dict # Librería que permite convertir mi modelo a tipo diccionario
from core.settings import MEDIA_URL, STATIC_URL
from apps.user.models import User
#from django.contrib.auth.models import User
from apps.srea.models import Asignatura
from datetime import date
from ckeditor.fields import RichTextField
import  random

##################Unidad####################
class Unidad(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    descripcion =models.TextField(verbose_name='Descripción')
    asignaturas=models.ManyToManyField(Asignatura, blank=True, related_name="asignaturas", verbose_name="Asignatura")

    def get_test(self):
        test_objs=list(Cuestionario.objects.filter(unidad=self))
        data = []
        for u_obj  in test_objs:
            print(u_obj)
            data.append(u_obj)
        return data

    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo, se convierte en un diccionario
        item['test']=[{'id':t.id, 'titulo':t.titulo}for t  in self.get_test()]
        item['asignaturas']=[{'id':c.id, 'nombre':c.nombre}for c  in self.asignaturas.all()]
        return item

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['id']

##################Quiz######################
class Cuestionario(models.Model):
    unidad = models.ManyToManyField(Unidad,blank=True,related_name="unidades", verbose_name="Unidad")
    titulo = models.CharField(max_length=150, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True,verbose_name="Descripción")
    numero_preguntas=models.IntegerField(verbose_name="Numero de preguntas")
    tiempo=models.IntegerField(verbose_name="Duración del Test")
    required_score_to_pass = models.IntegerField(verbose_name="Puntaje requerido")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación") 

    
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

##################Pregunta######################
class Pregunta(models.Model):
    test=models.ForeignKey(Cuestionario, on_delete=models.CASCADE, related_name="test")
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
        item['respuesta']= self.get_respuesta()
        return item

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['id']

##################Respuesta######################
class Respuesta(models.Model):
    pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="pregunta_respuesta")
    respuesta=models.TextField(verbose_name='Texto de la respuesta')
    correcta = models.BooleanField(default=False)


    def __str__(self):
        return self.respuesta

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['id']

##################Perfil--Resultado######################
class Resultado(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE, verbose_name="Cuestionario")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    score = models.FloatField(verbose_name="Puntaje")
    
    def __str__(self):
        return str(self.pk)
    
################################Borrador##########################################################3

class Answer(models.Model):
    answer_text=models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text
    
class Question(models.Model):
    question_text = models.CharField(max_length=900)
    answer = models.ManyToManyField(Answer)
    points = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    
class Quizzes(models.Model):#Cuestionarios
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    due = models.DateField()
    allowed_attemps = models.PositiveIntegerField()
    time_limit_mins = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title
    
class Attempter(models.Model): #Intentos
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    quiz= models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completed = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    
class Attempt(models.Model): #Intentar
    quiz= models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    attempter = models.ForeignKey(Attempter, on_delete=models.CASCADE)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.attempter.user.username + ' - ' + self.answer.answer_text
    

    

