from cProfile import label
from dataclasses import field, fields
import email
from tkinter import Widget
from turtle import mode
from django.forms import *

from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm #Importanto los formularios de Django
from django.contrib.auth import get_user_model, authenticate, login
User2 = get_user_model()

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
        model=Usuario
        fields=['email','username','nombres', 'apellidos']
        exclude = ['foto']

        widgets = {

            'email':EmailInput(
                attrs={
                    'class':'forms-control',
                    'placeholder':'Correo electrónico',

                }),

            'nombres':TextInput(
                attrs={
                    'class':'forms-control',
                    'placeholder':'Ingrese su nombre',

                }),
            'apellidos':TextInput(

                attrs={
                    'class':'forms-control',
                    'placeholder':'Ingrese sus apellidos',

                }),
            'username':TextInput(
                attrs={
                    'class':'forms-control',
                    'placeholder':'Ingrese su nombre de usuario',
                }),
        }


    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su constraseña...',
            'id':'password1',
            'required':'required',
        }
    ))

    password2 = forms.CharField(label='Contraseña de confirmación', widget=forms.PasswordInput(
         attrs={
            'class':'form-control',
            'placeholder':'Ingrese nuevamente su constraseña...',
            'id':'password2',
            'required':'required',
        }
    ))

    

    def clean_password2(self):#Validación de contraseña
        #Método que valida que ambas contraseñas ingresadas sean iguales, antes de ser encriptadas
        #y guardadas en la base de datos, se retorna la contraseña valida
        #
        #
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if  password1 != password2:
            raise forms.ValidationError('La clave no coincide')
        return password2

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ReporteCreateForm(ModelForm):
    class Meta:
        model= Reporte
        fields = ('titulo','descripcion','estado')

class IndicacionCreateForm(ModelForm):
    class Meta:
        model= Indicacion
        fields = ('titulo','descripcion')

class FichaCreateForm(ModelForm):
    class Meta:
        model= FichaInformacion
        #fields = ('descripcion','detalle_trabajo','detalle_ocupacion','detalle_tecnicaE', 'genero', 'etnia', 'estado_civil','user')
        fields= '__all__'
        exclude = ['foto']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class AsignaturaCreateForm(ModelForm):
    class Meta:
        model= Asignatura
        fields='__all__'
        exclude = ['foto','estado']
            
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class NivelCreateForm(ModelForm):
    class Meta:
        model= Nivel
        fields = ('nombre','numero', 'descripcion', 'estado')

class TestCreateForm(ModelForm):
    class Meta:
        model= Test
        fields = ('nombre', 'estado')


class PreguntaCreateForm(ModelForm):
    class Meta:
        model= Pregunta
        fields= '__all__'


