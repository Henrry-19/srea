from django.urls import path
from .views import CuentaDetailView, sreaListView, CuentaCreateView, CuentaUpdateView, CuentaDeleteView
from .views import UsuarioCreateView,UsuarioListView, UsuarioDeleteView,UsuarioUpdateView
from .views import ReporteListView,ReporteListPdf
from .views import IndicacionListView

app_name="srea"

urlpatterns = [
    path('',sreaListView.as_view(), name="home"),
    path('cuenta/', CuentaCreateView.as_view(), name="cuenta"),
    path('update/<int:pk>/', CuentaUpdateView.as_view(), name="update"),
    path('delete/<int:pk>', CuentaDeleteView.as_view(), name="delete"),
#-------------------------Usuario---------------------------------------
    path('u_lista/',UsuarioListView.as_view(), name="principal"),
    path('usuario/', UsuarioCreateView.as_view(), name="usuario"),
    path('u_lista/d_usuario/<int:pk>', UsuarioDeleteView.as_view(), name="d_usuario"),
    path('u_lista/u_usuario/<int:pk>/', UsuarioUpdateView.as_view(), name="u_usuario"),
#-------------------------Reporte---------------------------------------
    path('r_lista/',ReporteListView.as_view(), name="p_reporte"), #principal_reporte
    path('r_lista/r_lista_pdf/',ReporteListPdf.as_view(), name="reporte_pdf"), #principal_reporte
#-------------------------Reporte-----------------------------------------
    path('i_lista/',ReporteListView.as_view(), name="p_lista") #principal_indicacion

    
]


