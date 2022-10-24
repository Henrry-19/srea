from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View, UpdateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect

from apps.srea.forms import ReporteCreateForm
from apps.srea.models import Reporte

from django.urls import reverse_lazy

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


########################REPORTE##########################################3
class ReporteListView(View):
    def get(self,request, *args, **kwargs):
        reporte = Reporte.objects.all()
        context={
            'reporte':reporte
            
        }
        return render(request, 'reporte/reporte_lista.html', context)

#Reporte en pdf
class ReporteListPdf(View):
    def get(self,request, *args, **kwargs):
        try:
            template = get_template("reporte/reporte_imprimir.html")
            reporte=Reporte.objects.all()
            #reporte=Reporte.objects.get(pk=self.kwargs['pk'])
            context = {
                #'reporte': Reporte.objects.get(pk=self.kwargs['pk'])
                'reporte': reporte
            }
            html=template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            pisa_status = pisa.CreatePDF(
                html, dest=response)

            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('srea:p_reporte')) 


class ReporteCreateView(View):
    def get(self, request, *args, **kwargs):
        form=ReporteCreateForm()
        context={
            'form':form
        }
        return render(request, './reporte/reporte_create.html', context)

#Método para crear reporte   

    def post(self,request, *args, **kwargs):
        if request.method=="POST":#Si estámos enviando información a traves de un formulario
            form=ReporteCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                descripcion = form.cleaned_data.get('descripcion')
                estado =form.cleaned_data.get('estado')
                form.save()
        context={
            
        }
        return redirect('srea:p_reporte')
        #return render(request, 'cuenta/cuenta_create.html', context)

class ReporteDeleteView(DeleteView):
    model=Reporte
    template_name='reporte/reporte_delete.html'
    success_url=reverse_lazy('srea:p_reporte')

class ReporteUpdateView(UpdateView):
    model=Reporte
    fields=['titulo','descripcion','estado', 'user']
    template_name='reporte/reporte_update.html'

    def get_success_url(self): #Me regresa a la ventana
        pk = self.kwargs['pk']
        return reverse_lazy('srea:p_reporte')
