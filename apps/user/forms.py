from django.forms import*
from apps.user.models import User


class UserCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model=User
        fields= ['first_name','last_name','email', 'username', 'password', 'imagen', 'groups']
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
            })
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
                    user.groups.add(g)
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