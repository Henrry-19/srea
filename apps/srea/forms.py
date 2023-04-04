from django.forms import *
from apps.srea.models import*
from apps.user.models import*
from apps.quiz.models import*
from betterforms.multiform import MultiModelForm
from django import forms

class FacultadCreateForm(ModelForm):

    class Meta:
        model=Facultad
        fields= '__all__'

        widgets = {
                'carrera': SelectMultiple(attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'multiple': 'multiple'
                })
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

class CarreraCreateForm(ModelForm):

    class Meta:
        model=Carrera
        fields= ['facultad','nombre','duracion']

        widgets = {
           'facultad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
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



class AsignaturaCreateForm(ModelForm):

    class Meta:
        model=Asignatura
        fields= ['ciclo','nombre','detalle','imagen']

        widgets = {
           'users': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),
            'unidad': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),
            'ciclo': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                a=form.save()
                a.users.clear() #Limpia los grupos
                for u in self.cleaned_data['users']:
                    a.users.add(u)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class NewModuleForm(forms.ModelForm):
	#nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	#descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)

	class Meta:
		model = Unidad
		fields= ['nombre','descripcion','cuestionario']
        

class UnidadCreateForm(ModelForm):
    class Meta:
        model=Unidad
        fields= ['nombre','descripcion']

        widgets = {
           'cuestionario': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
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

        
class PreguntaCreateForm(ModelForm):

    class Meta:
        model=Pregunta
        fields= '__all__'

        widgets = {
           'test': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }#tipoPregunta

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


class RespuestaCreateForm(ModelForm):

    class Meta:
        model=Respuesta
        fields= ['respuesta']


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


class PreguntaRespuestaMultiForm(MultiModelForm):
    form_classes = {
        'pregunta': PreguntaCreateForm,
        'respuesta':RespuestaCreateForm,
    }







class CursoCreateForm(ModelForm):

    class Meta:
        model=Ciclo
        fields= ['nombre_ciclo','carrera']
        
        widgets = {
           'carrera': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
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