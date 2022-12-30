from django.urls import path
from apps.user.views import *


from django.contrib.auth.decorators import login_required

app_name="apps.user" #Variable que me permite decir como se va a llamar la ruta que se va a concatenar con la otra ruta absoluta

urlpatterns = [
#-------------------------Usuario---------------------------------------
    path('user_list/',(UserListView.as_view()), name="user_list"),
    path('user/', (UserCreateView.as_view()), name="user"),
    path('user_list/u_user/<int:pk>/', UserUpdateView.as_view(), name="u_user"),
    path('user_list/d_user/<int:pk>/', UserDeleteView.as_view(), name="d_user"),
    path('change/group/<int:pk>/', UserChangeGroup.as_view(), name='user_change_group'),
    path('perfil/', UserProfileView.as_view(), name='editar_perfil'),
    path('password/', UserChangePasswordView.as_view(), name='cambiar_clave'),

    ########################################################################3
    path('user/login', (UserCreateView2.as_view()), name="user_login"),

    
#-------------------------Reporte---------------------------------------

]


