from django import forms
from datetime import datetime
from django.forms import*
from apps.quiz.models import *
from ckeditor.widgets import CKEditorWidget
from django import forms
from apps.srea.models import (Catalog, CatalogItem)


class NewQuizForm(forms.ModelForm):
    #title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':' Título '}))
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['due'].widget.format = '%d/%m/%Y %H:%M'

    class Meta:
        model = Quiz
        #initial={'due':'05/01/2018',}
        fields = ('name','description') #allowed_attemps', 'time_limit_mins'
        
        widgets = {
                'name': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Título del Test'
                    
                }),

                #'due': DateTimeInput(attrs={'class': 'form-control'}),
        }



class NewQuestionForm(forms.ModelForm):
    #statement = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)


    class Meta:
        model = Question
        fields ='__all__'
        exclude =["external_id", "createdAt", "updatedAt", "state", "quiz"]

        labels = {
            "statement": "Enunciado",
            "type_question": "Tipo de pregunta",
        }
        help_texts = {
            "statement": "Ingrese el enunciado de su pregunta",
            "type_question": "Selecciona el tipo de pregunta",
        }
        widgets = {
            "statement": forms.Textarea(attrs={"class": "form-control", "rows": 2, "cols": 12}),
            "type_question": Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',}),
        }

class NewQuestionForm2(forms.ModelForm):
    #question_text = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)


    class Meta:
        model = Question
        fields ='__all__'
        exclude =['state','quiz']


        widgets = {
           'answers': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',
                    }),
        }




class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "description", "attempts", "time_limit", "start_date", "end_date"]
        exclude = ["external_id", "createdAt", "updatedAt", "state"]
        labels = {
            "name": "Nombre",
            "description": "Descripcion",
            "attempts": "Numero de Intentos",
            "time_limit": "Tiempo limite (HH:MM:SS)",
            "start_date": "Fecha de inicio (Y/M/D)",
            "end_date": "Fecha de finalizacion (Y/M/D)",
        }
        help_texts = {
            "name": "Ingresa el nombre del cuestionario",
            "description": "Ingresa la descripcion del cuestionario",
            "attempts": "Ingresa el numero de intentos del cuestionario",
            "time_limit": "Ingresa el tiempo limite del cuestionario",
            "start_date": "Ingresa la fecha de inicio del cuestionario",
            "end_date": "Ingresa la fecha de finalizacion del cuestionario",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}), 
            "description": forms.Textarea(attrs={"class": "form-control","placeholder": "Ingrese su observación", "rows": 3, "col": 12}),
            "attempts": forms.NumberInput(attrs={"class": "form-control"}), 
            "time_limit": forms.TimeInput(format="%H-%m-%s", attrs={"type": "time"}),
            "start_date": forms.DateInput(format="%Y-%m-%d", attrs={"value": datetime.now().strftime("%Y-%m-%d"), "type": "date"}),
            "end_date": forms.DateInput(format="%Y-%m-%d", attrs={"value": datetime.now().strftime("%Y-%m-%d"), "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields["name"].widget.attrs["autofocus"] = True
        self.fields["name"].widget.attrs["required"] = True

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ["external_id", "createdAt", "updatedAt", "state", "quiz"]
        labels = {
            "statement": "Enunciado",
            "type_question": "Tipo de pregunta",
        }
        help_texts = {
            "statement": "Ingrese el enunciado de su pregunta",
            "type_question": "Selecciona el tipo de pregunta",
        }
        widgets = {
            "statement": forms.Textarea(attrs={"class": "form-control", "rows": 2, "cols": 12}),
            "type_question": forms.Select(attrs={"class": "form-control"}),
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields["statement"].widget.attrs["autofocus"] = True
        self.fields["statement"].widget.attrs["required"] = True

class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = "__all__"
        exclude = ["external_id", "createdAt", "updatedAt", "state"]
        labels = {
            "statement": "Enunciado",
            "type_question": "Tipo de pregunta",
        }



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"
        exclude = ["external_id", "createdAt", "updatedAt", "state", "question"]
        labels = {
            "text": "Respuesta",
            "learning_style": "Estilo de enseñanza",
        }
        help_texts = {
            "text": "Ingrese la respuesta",
            "learning_style": "Selecciona el tipo de estilo de enseñanza",
        }
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 1, "cols": 12}),
            "learning_style": forms.Select(attrs={"class": "form-control select2", "style": "width: 100%"}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        learning_style = CatalogItem.objects.filter(catalog__code="ESTILOS_APRENDIZAJE", active=True)
        print("here ->", learning_style)
        self.fields["learning_style"].queryset = learning_style


AnswerFormSet = forms.inlineformset_factory(Question, Answer, form=AnswerForm, extra=1, can_delete=True)





class NewAnswerForm(forms.ModelForm):
    #text = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)
    #is_correct = forms.BooleanField(required=True)
    
    class Meta:
        model = Answer
        fields = ('text','learning_style')#'respuesta'