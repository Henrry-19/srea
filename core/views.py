from multiprocessing import context
from django.shortcuts import render
from django.views.generic import View 
from django.shortcuts import render  

class HomeView(View): #Primera vista
    def get(self, request, *args, **kwargs):#Modelo cliente - servidor (request)
        context={

        }
        return render(request, 'index.html',context)