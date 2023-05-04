from django.urls import path
from apps.user.views import *
from apps.srea.vistas.facultad import*
from apps.user.vistas.carerra import*
from apps.user.vistas.ficha import*


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
#-------------------------Facultad---------------------------------------
    path('facultad_list/',(FacultadListView.as_view()), name="facultad_list"),
    path('facultad/', (FacultadCreateView.as_view()), name="facultad"),
    path('facultad_list/u_facultad/<int:pk>/', FacultadUpdateView.as_view(), name="u_facultad"),
    path('facultad_list/d_facultad/<int:pk>/', FacultadDeleteView.as_view(), name="d_facultad"),

#-------------------------Carrera---------------------------------------
    path('carrera_list/',(CarreraListView.as_view()), name="carrera_list"),
    path('carrera/', (CarreraCreateView.as_view()), name="carrera"),
    path('carrera_list/u_carrera/<int:pk>/', CarreraUpdateView.as_view(), name="u_carrera"),
    path('carrera_list/d_carrera/<int:pk>/', CarreraDeleteView.as_view(), name="d_carrera"),

    #-------------------------Ficha---------------------------------------
    path('ficha_list/',(FichaListView.as_view()), name="ficha_list"),
    path('ficha/', (FichaCreateView.as_view()), name="ficha"),
    path('ficha_list/u_ficha/<int:pk>/',FichaUpdateView.as_view(), name="u_ficha"),
    path('ficha_list/d_ficha/<int:pk>/', FichaDeleteView.as_view(), name="d_ficha"),

    ###################################PDF###########################################
     path('ficha_list/pdf/<int:pk>/', FichaPdfView.as_view(), name="ficha_pdf"),

]


