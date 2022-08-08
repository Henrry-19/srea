from django.contrib import admin
from .models import Cuenta, Usuario,Reporte,FichaInformacion,Indicacion, Test, Pregunta, Nivel, Asignatura, User

# Register your models here.

admin.site.register(Cuenta)
admin.site.register(Usuario)
admin.site.register(Reporte)
admin.site.register(FichaInformacion)
admin.site.register(Indicacion)
admin.site.register(Test)
admin.site.register(Pregunta)
admin.site.register(Nivel)
admin.site.register(Asignatura)
admin.site.register(User)

