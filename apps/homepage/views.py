from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required #Importación de decoradores
from django.utils.decorators import method_decorator #Importación del método decorador
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class IndexView(LoginRequiredMixin,TemplateView):
    template_name='index.html'
