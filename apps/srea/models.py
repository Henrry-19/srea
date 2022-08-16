from distutils.command.upload import upload
from msilib.schema import Class
from pydoc import describe
from pyexpat import model
from turtle import up
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

estado_civil_ficha_informacion=(
    ('S','Soltero/a'),
    ('C','Casado/a'),
    ('D','Divorciado/a'),
    ('V','Viudo/a')
)
class FichaInformacion(models.Model):
    cedula=models.CharField(max_length=10)
    foto = models.ImageField(upload_to='cars')
    descripcion=models.TextField()
    edad=models.IntegerField()
    direccion=models.TextField()
    detalle_trabajo=models.TextField()
    detalle_ocupacion=models.TextField()
    detalle_tecnicaE=models.TextField()
    genero=models.CharField(choices=genero_ficha_informacion, max_length=1)
    etnia=models.CharField(max_length=50)
    estado_civil= models.CharField(choices=estado_civil_ficha_informacion, max_length=1)
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE)


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

class Pregunta(models.Model):
    pregunta=models.CharField(max_length=50)
    estado=models.BooleanField(default=False)
    user=models.ForeignKey(Test, on_delete=models.CASCADE)

class Respuesta(models.Model):
    respuesta=models.CharField(max_length=50)
    estado=models.BooleanField(default=False)
    user=models.ForeignKey(Pregunta, on_delete=models.CASCADE)




