from django.db import models
from datetime import datetime
from django.forms import model_to_dict # Librería que permite convertir mi modelo a tipo diccionario
from core.settings import MEDIA_URL, STATIC_URL

##################Usuario######################
genero_ficha_informacion = (
    ('female', 'Femenino'),
    ('male', 'Masculino')
)

class Usuario(models.Model):
    nombres=models.CharField(max_length=200, verbose_name='Nombres')
    apellidos=models.CharField(max_length=200, verbose_name='Apellidos')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    email=models.EmailField(max_length=254,unique=True,verbose_name='Correo Electrónico')
    genero = models.CharField(max_length=10, choices=genero_ficha_informacion, default='male', verbose_name='Genero')
    
 ###Crear un método llamado toJSON###
    def toJSON(self):##Me devuelve un diccionario con todos los atributos de mi entidad
        item=model_to_dict(self) #Mi atributo self contiene mi modelo
        return item

    def __str__(self): 
        return f'{self.nombres},{self.apellidos}'
    
    class Meta:
        verbose_name = 'Usuarios'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']
    


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

##################Ficha de información######################

class FichaInformacion(models.Model):
    user= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    edad=models.IntegerField()
    direccion=models.CharField(max_length=50)
    ocupacion=models.CharField(max_length=50) #Ingresar como lista-clase ocupación
    tecnica_estudio=models.CharField(max_length=50,null=True)
    etnia=models.CharField(choices=etnia_ficha,max_length=10)
    estado_civil= models.CharField(choices=estado_civil_ficha_informacion, max_length=10)
    

    def __str__(self):
        return self.cedula #llamar con clave primaria
    
    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['id']

##################Indicación######################
class Indicacion(models.Model):
    user= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo=models.CharField(max_length=100)
    descripcion=models.TextField(verbose_name='Descripción')
    fecha=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Indicación'
        verbose_name_plural = 'Indicaciones'
        ordering = ['id']

##################Asignatura######################    
class Asignatura(models.Model):
    user= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    detalle=models.TextField(verbose_name='Detalle de la asignatura')
    imagen = models.ImageField(upload_to='asignatura/%Y/%m/%d', null=True, blank=True)
    
    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def __str__(self):
        return self.nombre 

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['id']   

##################Nivel######################
class Nivel(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    descripcion=models.TextField(verbose_name='Descripción')
   
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'
        ordering = ['id']

##################Test######################

class Test(models.Model):
    nivel= models.ForeignKey(Nivel, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['id']
   

##################Pregunta######################

class Pregunta(models.Model):
    test=models.ForeignKey(Test, on_delete=models.CASCADE)
    texto=models.TextField(verbose_name='Texto de la pregunta')

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['id']  

##################Respuesta######################

class Respuesta(models.Model):
    pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta=models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.respuesta

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['id']  






