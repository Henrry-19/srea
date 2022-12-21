from django.urls import path
from apps.user.views import *


from django.contrib.auth.decorators import login_required

app_name="apps.user" #Variable que me permite decir como se va a llamar la ruta que se va a concatenar con la otra ruta absoluta

urlpatterns = [
#-------------------------Usuario---------------------------------------
    path('user_list/',(UserListView.as_view()), name="user_list"),
    path('user/', (UserCreateView.as_view()), name="user"),
    path('u_lista/u_usuario/<int:pk>/', UserUpdateView.as_view(), name="u_user"),
#    path('u_lista/d_usuario/<int:pk>/', UsuarioDeleteView.as_view(), name="d_usuario"),
#-------------------------Reporte---------------------------------------

]


