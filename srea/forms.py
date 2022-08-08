from dataclasses import field, fields
from turtle import mode
from django.forms import  ModelForm 

from .models import Asignatura, Cuenta, Nivel, Reporte,Usuario, Reporte, Indicacion, Test, Pregunta, FichaInformacion

 
class CuentaCreateForm(ModelForm):
    class Meta: 
        model = Cuenta
        fields = ('user','correo','clave','estado')

class UsuarioCreateForm(ModelForm):
    class Meta:
        model= Usuario
        fields = ('cedula','apellido','nombre','fecha_nacimiento','edad','direccion', 'foto', 'id_usuario')

class ReporteCreateForm(ModelForm):
    class Meta:
        model= Reporte
        fields = ('titulo','descripcion','estado','user')

class IndicacionCreateForm(ModelForm):
    class Meta:
        model= Indicacion
        fields = ('titulo','descripcion','user')

class FichaCreateForm(ModelForm):
    class Meta:
        model= FichaInformacion
        fields = ('descripcion','detalle_trabajo', 'detalle_ocupacion', 'genero', 'etnia', 'estado_civil','user')

class AsinaturaCreateForm(ModelForm):
    class Meta:
        model= Asignatura
        fields = ('nombre','detalle', 'foto', 'estado','user')


class NivelCreateForm(ModelForm):
    class Meta:
        model= Nivel
        fields = ('nombre','numero', 'descripcion', 'estado','user')

class TestCreateForm(ModelForm):
    class Meta:
        model= Test
        fields = ('nombre', 'estado','user')

class PreguntaCreateForm(ModelForm):
    class Meta:
        model= Pregunta
        fields = ('pregunta', 'estado','user')