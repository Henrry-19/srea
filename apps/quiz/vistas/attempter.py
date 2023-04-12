from django.views.generic import* #importando la vista genérica
from django.contrib.auth.decorators import login_required
from django.http import *
from django.urls import reverse_lazy
from apps.srea.mixins import*
from apps.srea.forms import*
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def ListarResultadosEstudiantes(request):
        user=request.user
        lista=''
        if request.user.is_staff:
                lista=Attempter.objects.all()
        else:
                lista=Attempter.objects.filter(user=user)
                #print(lista)
        context = {
                    'lista': lista,
                    'title':'Resultados', #Puedo enviar variables
        }

        return render(request, 'attempter/attempter_resultado.html', context)
