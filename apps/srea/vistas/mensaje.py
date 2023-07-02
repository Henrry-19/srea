from django.shortcuts import render
from apps.user.models import*
from apps.srea.mixins import*
from django.views.generic import* #importando la vista genérica
from django.http import *
from apps.srea.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from apps.srea.models import*
from django.contrib.auth.decorators import *

   
@login_required
@permission_required('srea.view_mensajenasignatura')
def MensajeAsignatura(request, asignatura_id):
    asigna = get_object_or_404(Asignatura, id=asignatura_id)
    
    if request.user.is_staff : 
        mensaje = MensajenAsignatura.objects.filter(asignatura=asigna)
    if  not request.user.is_staff:
        mensaje = MensajenAsignatura.objects.filter(asignatura=asigna)
        #data.append(mensaje)
        

    context={
            'mensaje':mensaje,
            'asigna': asigna,
            'url_create':reverse_lazy('srea:crear_mensajes'),
            'list_url':reverse_lazy('user:mensaje_asignatura'),
            'title':'Lista de mensajes',
            'modelo':'Mensajes',
            'date_now':datetime.now()  
    }

    return render(request, 'mensaje_asignatura/mensaje_lista.html', context)
    

@login_required
@permission_required('srea.view_mensajenasignatura')
def MensajeDetail(request, mensajenasignatura_id):
        #asignatura_pk=decrypt(asignatura_pk)
        user = request.user
        mensaje = get_object_or_404(MensajenAsignatura, id=mensajenasignatura_id)
        teacher_mode=False
        #print(asigna.unidad)
   
        context = {
            'mensaje': mensaje,
            #'user_id':user_id,
            'modelo':'Mensajes'
        }

        return render(request, 'mensaje_asignatura/mensaje_lista_user.html', context)

@login_required
@permission_required('srea.add_mensajenasignatura')
def MensajeCreate(request, asignatura_id):
    #user=request.user
    if not request.user.is_staff:
        if request.method == 'POST':
            form = MensajeCreateForm(request.POST, request.FILES, request=request)
            if form.is_valid():
                titulo=form.cleaned_data.get('titulo')
                descripcion=form.cleaned_data.get('descripcion')
                asignatura=form.cleaned_data.get("asignatura")
                fecha=form.cleaned_data.get("fecha")
                m = MensajenAsignatura.objects.create(titulo=titulo,descripcion=descripcion,fecha=fecha,asignatura=asignatura)#
                            #course.unidad.add(m)# registramos la unidad en la asignatura
                m.save()
                return redirect('srea:mensaje_asignatura', asignatura_id=asignatura_id)
        else:
            form = MensajeCreateForm(request=request)
    else:
        return HttpResponseForbidden("No tiene permiso para ingresar a este módulo")
    context={
            'form': form,
            'asignatura_id':asignatura_id,
            'url_list':reverse_lazy('srea:mensaje_asignatura')
            }
    return render(request, 'mensaje_asignatura/mensaje_create.html', context)


@login_required
@permission_required('srea.change_mensajenasignatura')
def MensajeUpdateView(request, asignatura_id, mensajenasignatura_id):#Editar mensaje
    mensaje = get_object_or_404(MensajenAsignatura, id=mensajenasignatura_id)
    if request.method == 'POST':
        form = MensajeModificarForm(request.POST, request.FILES, instance=mensaje)
        if form.is_valid():
            mensaje.titulo = form.cleaned_data.get('titulo')
            mensaje.descripcion = form.cleaned_data.get('descripcion')
            mensaje.save()   
            return redirect('srea:mensaje_asignatura', asignatura_id=asignatura_id)
    else:
        form = MensajeModificarForm(instance=mensaje)

    context = {
		'form': form,
		'mensaje': mensaje,
        'asignatura_id':asignatura_id,
        'url_list': reverse_lazy('srea:mensaje_asignatura'),
	}
    return render(request, 'mensaje_asignatura/mensaje_create.html', context)

@login_required
@permission_required('srea.delete_mensajenasignatura')
def EliminarMensaje(request, asignatura_id,mensajenasignatura_id):
   mensaje = get_object_or_404(MensajenAsignatura, id=mensajenasignatura_id)
   context={
        'mensaje':mensaje,
        'asignatura_id':asignatura_id,
        'modelo':"Mensaje",
    }
   if request.method=="POST":
       mensaje.delete()
       return redirect('srea:mensaje_asignatura', asignatura_id=asignatura_id)
   
    
   return render(request, 'mensaje_asignatura/mensaje_delete.html',context)