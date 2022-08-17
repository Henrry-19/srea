from cProfile import label
from dataclasses import field, fields
from tkinter import Widget
from turtle import mode
from django.forms import *

from .models import Asignatura, Cuenta, Nivel, Reporte,Usuario, Reporte, Indicacion, Test, Pregunta, FichaInformacion

 
class CuentaCreateForm(ModelForm):
    class Meta: 
        model = Cuenta
        fields= '__all__'
        #exclude = ['user']

        widgets = {
            'correo': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Ingrese el correo',
                'autocomplete':'off',
                 }),
            'clave': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Ingrese la clave',
                'autocomplete':'off',
                'type':'password'
                 }),         
        }
      
        

class UsuarioCreateForm(ModelForm):
    class Meta:
        model= Usuario
        fields= '__all__'
        exclude = ['estado']
        widgets = {
            'nombre': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Nombre',
                'autocomplete':'off',
                 }),  

            'apellido': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Apellido',
                'autocomplete':'off',
                 }),
            
            'correo': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Correo electrónico',
                'autocomplete':'off',
                 }),

            'clave': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Contraseña nueva',
                'autocomplete':'off',
                'type':'password',
                 }),

            'fecha_nacimiento': TextInput(attrs={
                'type':'date',
                 }),
                     
        }

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
        fields = ('descripcion','detalle_trabajo','detalle_ocupacion','detalle_tecnicaE', 'genero', 'etnia', 'estado_civil','user')

class AsignaturaCreateForm(ModelForm):
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