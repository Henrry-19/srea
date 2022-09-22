from cProfile import label
from dataclasses import field, fields
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
    def _init_(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields(): #Recorrer los componentes de mi formulario
            form.field.widget.attrs['class']= 'form-control'
            form.field.widget.attrs['autocomplete']= 'off'
    class Meta:
        model= Usuario
        fields= '__all__'
        exclude = ['estado']
        widgets = {
            'nombre': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Nombre',
                 }),  

            'apellido': TextInput(attrs={
                'class':'col-auto',
                'placeholder':'Apellido',
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
# 'rows':3,
# 'cols':3}
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
        #fields = ('descripcion','detalle_trabajo','detalle_ocupacion','detalle_tecnicaE', 'genero', 'etnia', 'estado_civil','user')
        fields= '__all__'
        #exclude = ['estado']

class AsignaturaCreateForm(ModelForm):
    class Meta:
        model= Asignatura
        fields='__all__'
        exclude = ['estado']


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
        fields= '__all__'

class ElegirRespuestaCreateForm(ModelForm):
    class Meta:
        model= ElegirRespuesta
        fields= '__all__'
#

class ElegirInlineFormset(forms.BaseInlineFormSet):
    def clean(self):#Función limpiar
        super(ElegirInlineFormset, self).clean() #
        respuesta_correcta=0
        for formulario in self.forms:
            if not formulario.is_valid(): #Si nuestro formulario no es valido
                return 
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta +=1 #Vamos  a ir iterando la respuesta
        try:
            assert respuesta_correcta==Pregunta.NUMER_DE_RESPUESTAS_PERMITIDAS
        except AssertionError:
            raise forms.ValidationError('Solo se permite una respuesta')
        

class UsuarioLoginFormulario(forms.Form):
    username = forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user2= authenticate(username=username, password=password) 
            if not user2:
                raise forms.ValidationError('No existe el usuario')
            if not user2.check_password(password):
                raise forms.ValidationError('Contraseña incorrecta')
            if not user2.is_active:
                raise forms.ValidationError('El usuario no está activo')
        return super(UsuarioLoginFormulario, self).clean(*args,**kwargs)

    
#Clase para registrar el formulario de un usuario 
class RegistroFormulario(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User2
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]
