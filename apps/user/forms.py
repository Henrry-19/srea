from django.forms import*

from apps.user.models import User

class UserCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model=User
        fields= ['first_name','last_name','email', 'username', 'password', 'imagen']
        exclude = ['groups', 'last_login' , 'date_joineds', 'is_superuser', 'is_active', 'is_staff', 'user_permissions']

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