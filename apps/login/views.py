from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import *
from django.views.generic import RedirectView,FormView
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #importando el método decorador
from django.views.decorators.csrf import csrf_exempt
from apps.login.forms import*
from django.http import *
import smtplib
import uuid #Permite generar un código universal de encriptación
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string




class LoginFormView(LoginView):
    template_name='login.html'
    #success_url= reverse_lazy('login:index1') #Me redirecciona la URL y reverse_lazy->devuelve la ruta de la URL
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL) #Enviado esa dirección
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Iniciar sesión'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name='login' #El nombre del patrón de URL al que se redirigirá.
    
  
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name= 'login/reset_password.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    
    @method_decorator(csrf_exempt)#Mecanismo de defensa de django
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_pwd(self, user):
            data = {}
            try:
                URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
                user.token = uuid.uuid4()
                user.save()

                mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                mailServer.starttls()
                mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                email_to = user.email
                mensaje = MIMEMultipart()
                mensaje['From'] = settings.EMAIL_HOST_USER
                mensaje['To'] = email_to
                mensaje['Subject'] = 'Reseteo de contraseña'

                content = render_to_string('login/send_email.html', {
                    'user': user,
                    'link_resetpwd': 'http://{}/change/password/{}/'.format(URL, str(user.token)),
                    'link_home': 'http://{}'.format(URL)
                })
                mensaje.attach(MIMEText(content, 'html'))

                mailServer.sendmail(settings.EMAIL_HOST_USER,
                                    email_to,
                                    mensaje.as_string())
            except Exception as e:
                data['error'] = str(e)
            return data

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user=form.get_user()
                data=self.send_email_reset_pwd(user)
            else:
                data['error'] =form.errors
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Reseteo de Clave'
        return context
    

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name= 'login/change_password.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    
    @method_decorator(csrf_exempt)#Mecanismo de defensa de django
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):###Implementación de ajax en mi método sobrescrito POST###
        data={} #Se declara un diccionario llamado data
        try: #controlar el error
            pass
        except Exception as e: #Llamamos a la clase Exceptio para indicar el error
            data['error']=str(e) #Me devuelve el objeto e-->convertido a un string
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Reseteo de Clave'
        return context
    



