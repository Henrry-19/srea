from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.contrib.auth import logout

class LoginFormView(LoginView):
    template_name='login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('srea:principal')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Iniciar sesión'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name='login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

