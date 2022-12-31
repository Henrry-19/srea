from django.contrib import admin
from .models import *

admin.site.site_header = 'Admin SREA'
admin.site.index_title = 'Panel de Control'

# ASIGNATURAS
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ["user", 'nombre','detalle', 'imagen']
    search_fields = ['nombre']
    ordering = ['user']

admin.site.register(Asignatura, AsignaturaAdmin)

# Register your models here.
#admin.site.register(Usuario)
#-------------------------------------
#admin.site.register(FichaInformacion)
#admin.site.register(Indicacion)

#admin.site.register(Nivel)
#admin.site.register(Test)
#admin.site.register(Pregunta)
#admin.site.register(Respuesta)






