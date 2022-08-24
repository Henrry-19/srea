from django.contrib import admin
from .models import *
from .forms import  ElegirInlineFormset

admin.site.register(PreguntasRespondidas)
admin.site.register(ElegirRespuesta)


# Register your models here.

admin.site.register(Cuenta)
admin.site.register(Usuario)
admin.site.register(Reporte)
admin.site.register(FichaInformacion)
admin.site.register(Indicacion)
admin.site.register(Test)
admin.site.register(Nivel)
admin.site.register(Asignatura)
admin.site.register(User)



#Heredar desde elegir respuesta los campos del texto y observarlo en nuestra pregunta 
class ElegirRespuestaInline(admin.TabularInline):#Instanciar nuestro método Elegir respuesta
    model= ElegirRespuesta
    can_delete = False
    max_num= ElegirRespuesta.MAXIMO_RESPUESTA
    min_num= ElegirRespuesta.MAXIMO_RESPUESTA
    formset = ElegirInlineFormset
    

class PreguntaAdmin(admin.ModelAdmin):
    model= Pregunta
    inlines=(ElegirRespuestaInline,)
    list_display = ['texto',]
    search_fields = ['texto','preguntas__texto'] #Campos de búsqueda, una posible respuesta


class PreguntasRespondidasAmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidas


admin.site.register(Pregunta, PreguntaAdmin)
