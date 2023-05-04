from django import forms
from django.forms import*
from apps.quiz.models import *
from ckeditor.widgets import CKEditorWidget
from django import forms


class NewQuizForm(forms.ModelForm):
    #title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':' Título '}))
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['due'].widget.format = '%d/%m/%Y %H:%M'

    class Meta:
        model = Quizzes
        #initial={'due':'05/01/2018',}
        fields = ('cat','title', 'description', 'due', 'allowed_attemps', 'time_limit_mins')
        
        widgets = {
                'title': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Título del Test'
                    
                }),

                'cat': Select(attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                }),

                #'due': DateTimeInput(attrs={'class': 'form-control'}),

                'allowed_attemps': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Número de intentos'
                    
                }),

                'time_limit_mins': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Tiempo limite'
                    
                }),
        }



class NewQuizForm2(forms.ModelForm):

    class Meta:
        model = Quizzes
        #initial={'due':'05/01/2018',}
        fields = ('title', 'description', 'due', 'allowed_attemps', 'time_limit_mins')
        
        widgets = {
                'title': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Título del Test'
                    
                }),

                'cat': Select(attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                }),

                #'due': DateTimeInput(attrs={'class': 'form-control'}),

                'allowed_attemps': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Número de intentos'
                    
                }),

                'time_limit_mins': TextInput(attrs={
                    'class': 'form-control',
                    'autocomplete':'off',
                    'placeholder':' Tiempo limite'
                    
                }),
        }



class NewQuestionForm(forms.ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)


    class Meta:
        model = Question
        fields ='__all__'
        exclude =['answers']

class NewQuestionForm2(forms.ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)


    class Meta:
        model = Question
        fields ='__all__'
        #exclude =['answers']

        widgets = {
           'answers': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',
                    }),
        }


class NewAnswerForm(forms.ModelForm):
    answer_text = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)
    #is_correct = forms.BooleanField(required=True)
    
    class Meta:
        model = Answer
        fields = ('answer_text', 'respuesta')