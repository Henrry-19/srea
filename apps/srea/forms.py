from django.forms import *
from apps.srea.models import*
from apps.user.models import*


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
        fields= ['nombre','duracion','curso']

        widgets = {
           'curso': SelectMultiple(attrs={
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
        fields= ['users','nombre','detalle','imagen']

        widgets = {
           'users': SelectMultiple(attrs={
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
    
    

class PreguntaCreateForm(ModelForm):

    class Meta:
        model=Pregunta
        fields= '__all__'

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


class CursoCreateForm(ModelForm):

    class Meta:
        model=Curso
        fields= ['nombre_ciclo','asignatura']
        
        widgets = {
           'asignatura': SelectMultiple(attrs={
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