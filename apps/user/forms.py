from django.forms import*
from django import forms
from apps.user.models import *
from apps.srea.models import *


class FichaCreateForm(forms.ModelForm):
    #first_name = forms.CharField(max_length = 50)
    class Meta:
        model=Ficha
        fields= '__all__'

        widgets = {
            'user': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),
            'genero': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'etnia': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'estado_civil': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'nacionalidad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),

            
            'ocupacion': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),

            
            'tecnica_estudio': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #if self.instance.id and self.instance.user:
        #    self.fields['user'].widget.attrs.update({'disabled': True})


    def __init__(self, *args, **kwargs): ###Filtrado
        self.request = kwargs.pop("request")
        super(FichaCreateForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_staff:
            self.fields["user"].queryset = User.objects.filter(id=self.request.user.id)
            
        #    if self.instance.pk and self.instance.user:
        #        self.fields['user'].widget.attrs.update({'disabled': True})



    def save(self, commit=True):
        data = {}
        form = super()
        #ficha = super().save(commit=True)
        #ficha.user.first_name = first_name
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    

class EditarFichaCreateForm(ModelForm):
    class Meta:
        model=Ficha
        fields= ['dni','birthday','genero', 'direccion', 'ocupacion', 'tecnica_estudio','etnia','nacionalidad','estado_civil']
        exclude =['user']

        widgets = {
            'genero': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'etnia': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'estado_civil': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'nacionalidad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }
    
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
        
    #    if self.instance.pk and self.instance.user:
    #        self.fields['user'].widget.attrs.update({'disabled': True})


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

class UserCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model=User
        fields= ['first_name','last_name','email', 'username', 'password', 'imagen','groups']
        exclude = ['last_login' , 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'user_permissions']

        widgets = {
            'first_name':TextInput(
                attrs={
                    'placeholder':'Ingrese su nombre'
                }
            ),
            'last_name':TextInput(
                attrs={
                    'placeholder':'Ingrese su apellido'
                }
            ),
            'email':TextInput(
                attrs={
                    'placeholder':'Ingrese su email'
                }
            ),
            'username':TextInput(
                attrs={
                    'placeholder':'Ingrese un nombre de usuario'
                }
            ),
            'password':PasswordInput(render_value=True,
                attrs={
                    'placeholder':'Ingrese su password',
                }
            ),
            'groups': SelectMultiple(attrs={
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
                pwd=self.cleaned_data['password']
                u=form.save(commit=False) #Hacemos una pausa a la creación del objeto
                if u.pk is None:
                    u.set_password(pwd)
                else:
                     user=User.objects.get(pk=u.pk)
                     if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                ###########Groups#################
                u.groups.clear() #Limpia los grupos
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
                ###########Cursos#################
                #u.curso.clear() #Limpia los cursos
                #for c in self.cleaned_data['curso']:
                #    u.curso.add(c)

            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model=User
        fields= ['first_name','last_name','email', 'username','password','imagen']
        exclude = ['last_login' , 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'user_permissions', 'groups']

        widgets = {
            'first_name':TextInput(
                attrs={
                    'placeholder':'Ingrese su nombre'
                }
            ),
            'last_name':TextInput(
                attrs={
                    'placeholder':'Ingrese su apellido'
                }
            ),
            'email':TextInput(
                attrs={
                    'placeholder':'Ingrese su email'
                }
            ),
            'username':TextInput(
                attrs={
                    'placeholder':'Ingrese un nombre de usuario'
                }
            ),
            'password':PasswordInput(render_value=True,
                attrs={
                    'placeholder':'Ingrese su password',
                }
            )
        }
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd=self.cleaned_data['password']
                u=form.save(commit=False) #Hacemos una pausa a la creación del objeto
                if u.pk is None:
                    u.set_password(pwd)
                else:
                     user=User.objects.get(pk=u.pk)
                     if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserCreateForm2(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model=User
        fields= ['first_name','last_name','email', 'username', 'password']
        exclude = ['last_login' , 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'user_permissions']

        widgets = {
            'first_name':TextInput(
                attrs={
                    'placeholder':'Ingrese su nombre'
                }
            ),
            'last_name':TextInput(
                attrs={
                    'placeholder':'Ingrese su apellido'
                }
            ),
            'email':TextInput(
                attrs={
                    'placeholder':'Ingrese su email'
                }
            ),
            'username':TextInput(
                attrs={
                    'placeholder':'Ingrese un nombre de usuario'
                }
            ),
            'password':PasswordInput(render_value=True,
                attrs={
                    'placeholder':'Ingrese su password',
                }
            )
        }
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd=self.cleaned_data['password']
                u=form.save(commit=False) #Hacemos una pausa a la creación del objeto
                if u.pk is None:
                    u.set_password(pwd)
                else:
                     user=User.objects.get(pk=u.pk)
                     if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear() #Limpia los grupos
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class IndicacionCreateForm(ModelForm):

    class Meta:
        model=Indicacion
        fields= '__all__'

        widgets = {
            'user': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),
            'genero': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'etnia': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'estado_civil': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),

            'nacionalidad': Select(attrs={
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
    
