from django.views.generic import TemplateView


class Index1View(TemplateView):
    template_name = 'index1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        return context
