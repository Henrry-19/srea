from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index1.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def get_graph_estilos_a(self): #Se debe trabjar en este método
        year = datetime.now().year

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_estilos_a'] = []
        return context


class IndexViewAsignatura(LoginRequiredMixin,TemplateView):
    template_name = 'htz/body.html'

def index(request):
	user = request.user
    

	#courses = Course.objects.filter(enrolled=user)

	#context = {
	#	'courses': courses
	#}
	return render(request, 'index.html')