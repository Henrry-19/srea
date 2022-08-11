from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from srea.forms import TestCreateForm
from srea.models import Test

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


########################Test##################################################


class TestListView(View):
    def get(self,request, *args, **kwargs):
        test = Test.objects.all()
        context={
            'test':test
            
        }
        return render(request, 'test/test_lista.html', context)


class TestCreateView(View):
    def get(self, request, *args, **kwargs):
        form=TestCreateForm()
        context={
            'form':form
        }
        
        return render(request, './test/test_create.html', context)

#Método para crear test
    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=TestCreateForm(request.POST)
            if form.is_valid():
                nombre=form.cleaned_data.get('nombre')
                user=form.cleaned_data.get('user')
                estado=form.cleaned_data.get('estado')
                form.save()
                
        context={
            
        }
        return redirect('srea:p_test')


class TestDeleteView(DeleteView):
    model=Test
    template_name='test/test_delete.html'
    success_url=reverse_lazy('srea:p_test')

class TestUpdateView(UpdateView):
    model=Test
    fields=['nombre', 'user', 'estado']
    template_name='test/test_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_test')