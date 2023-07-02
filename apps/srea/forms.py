from django.forms import *
from apps.srea.models import*
from apps.user.models import*
from apps.quiz.models import*

from django import forms

class CatalogoCreateForm(ModelForm):

    class Meta:
        model=Catalog
        fields= '__all__'

        labels = {
            "active": "Estado",
            "code": "Código",
            "name": "Nombre",
            "description": "Descripción",
            "order": "Orden",
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
    
class CatalogoItemCreateForm(ModelForm):

    class Meta:
        model=CatalogItem
        fields= '__all__'

        labels = {
            "active": "Estado",
            "code": "Código",
            "name": "Nombre",
            "description": "Descripción",
            "order": "Orden",
            "catalog": "Catálogo",
        }

        widgets = {
                'catalog': Select(attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
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



class AsignaturaCreateForm(forms.ModelForm):
    class Meta:
        model=Asignatura
        fields= ['ciclo','nombre','detalle','imagen']
        #docente=
        widgets = {
           'users': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',
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
            'docente': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',     
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
    

class AsignaturaModificarCreateForm(forms.ModelForm):
    class Meta:
        model=Asignatura
        fields= ['nombre','detalle','imagen']
        #exclude=['docente','ciclo']
        widgets = {
           'users': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',
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
            'docente': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',     
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
		fields= ['nombre','descripcion']
        

class UnidadCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':' Unidad I - Asignatura '}))
    class Meta:
        model=Unidad
        fields= ['nombre','descripcion']

        widgets = {
           'quizzes': SelectMultiple(attrs={
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

class RegistrarQuizForm(forms.ModelForm):
    #nombre = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':' Unidad I '}))
    class Meta:
        model=UnidadQuiz
        fields= ['quiz','unidad']

        widgets = {
           'quiz': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'simple': 'simple',
            }),
            'unidad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'simple': 'simple',
            }),
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def __init__(self, *args, **kwargs): ###Filtrado
        self.request = kwargs.pop("request")
        super(RegistrarQuizForm, self).__init__(*args, **kwargs)
        asignatura=Asignatura.objects.filter(users=self.request.user)
        if not (self.request.user.is_staff):
            self.fields["unidad"].queryset = Unidad.objects.filter(unidad_asignatura__in=asignatura)
        else:
            self.fields["unidad"].queryset = Unidad.objects.all()
            
        #print("-->TOBY",asignatura)
        
class RegistrarQuizUserForm(forms.ModelForm):
    #nombre = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':' Unidad I '}))
    class Meta:
        model=UserQuiz
        fields= ['quiz','users']

        widgets = {
           'quiz': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'simple': 'simple',
            }),
            'users': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),
        }



class UnidadEditarCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':' Unidad I - Asignatura '}))
    class Meta:
        model=Unidad
        fields= ['nombre','descripcion']#,'cuestionario'
        #exlude=['quizzes']

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


class CursoCreateForm(forms.ModelForm):
    nombre_ciclo = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Ciclo I - Nombre de la carrera '}))

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
    

class MensajeCreateForm(ModelForm):

    class Meta:
        model=MensajenAsignatura
        fields= ['asignatura','titulo','descripcion']
        #exclude = ['asignatura']

        widgets = {
            'asignatura': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def __init__(self, *args, **kwargs): ###Filtrado
        self.request = kwargs.pop("request")
        super(MensajeCreateForm, self).__init__(*args, **kwargs)
        self.fields["asignatura"].queryset = Asignatura.objects.filter(users=self.request.user)
       
    

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
    
class MensajeModificarForm(ModelForm):

    class Meta:
        model=MensajenAsignatura
        fields= ['titulo','descripcion']
        #exclude = ['']
       
    

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
    
class FileUploadedForms(forms.ModelForm):
    class Meta:
        model = FileUploaded
        fields ="__all__"

        widgets = {
            "file": forms.ClearableFileInput(),
            "observation": forms.Textarea(attrs={"placeholder": "Ingrese su observación", "rows": 3}),
        }

#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs['request'] = self.request
#        return kwargs
    
 #   def __init__(self, *args, **kwargs): ###Filtrado
 #       self.request = kwargs.pop("request")
 #       super(FileUploadedForms, self).__init__(*args, **kwargs)
 #       self.fields["observation"].widget.attrs["autofocus"] = True
 #       self.fields["observation"].widget.attrs["required"] = True
 #       asignatura=Asignatura.objects.filter(users=self.request.user)
 #       if not (self.request.user.is_staff):
 #           self.fields["unid"].queryset = Unidad.objects.filter(unidad_asignatura__in=asignatura)
 #       else:
 #           self.fields["unid"].queryset = Unidad.objects.all()





#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)        
#        self.fields["observation"].widget.attrs["autofocus"] = True
#        self.fields["observation"].widget.attrs["required"] = True


class SubirArchivoForms(forms.ModelForm):
    class Meta:
        model = SubirArchivos
        fields ="__all__"

        widgets = {
            "archivo": forms.ClearableFileInput(),
            "observación": forms.Textarea(attrs={"placeholder": "Ingrese su observación", "rows": 3}),
        }