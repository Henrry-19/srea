from django.views.generic import* #importando la vista genérica
from apps.srea.models import  Asignatura #importando los modelos
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render, redirect, get_object_or_404
from apps.srea.mixins import*
from apps.srea.forms import*
from django.contrib.auth.decorators import permission_required



@login_required
#@permission_required('quiz.add_quiz')
def RegistrarQuizUser(request, asignatura_id):
    asigna = get_object_or_404(Asignatura, id=asignatura_id)
    if request.method == 'POST':
        form = RegistrarQuizUserForm(request.POST, request.FILES)
        if form.is_valid():
            quiz=form.cleaned_data.get('quiz')
            users=form.cleaned_data.get('users')
            m = UserQuiz.objects.create(quiz=quiz)
            for u in users:
                m.users.add(u)
                u.save()
            return redirect('srea:primeraU', asignatura_id=asignatura_id)
    else:
        form = RegistrarQuizUserForm()

        context = {
		'form': form,
        'asignatura_id':asignatura_id,
        'asigna':asigna,
        #'url_list':reverse_lazy('srea:p_asignatura')
	    }
        return render(request, 'user_quiz/registrar_quiz_user.html', context)


@login_required#Sirve
@permission_required('quiz.view_quiz')
def QuizDetailUser(request,asignatura_id,external_id):
    #user = request.user
    quiz=get_object_or_404(Quiz, id=external_id)
    context={
        'quiz':quiz,
        'asignatura_id':asignatura_id,
    }

    return render(request, 'user_quiz/quiz_detail_user.html', context)


@login_required#Sirve-->Con este método estoy listando las preguntas y respuestas del cuestionario
@permission_required('quiz.view_quiz')
def TakeQuizUser(request,asignatura_id, quiz_id):#Tomar el cuestionario
    quiz=get_object_or_404(Quiz, id=quiz_id)
    questions=Question.objects.filter(quiz=quiz.id)

    context={
        'quiz':quiz,
        'question':questions,
        'asignatura_id':asignatura_id,
    }
    
    return render(request, 'user_quiz/take_quiz_user.html', context)


@login_required#sirve
@permission_required('quiz.view_quiz')
def SubmitAttemptUser(request,asignatura_id,quiz_id):#Envíar intento-->Podemos reutilizar este método
    user=request.user
    quiz=get_object_or_404(Quiz, id=quiz_id)
    #intentos=0
    #print("--->Modelo",quiz)

    if request.method=='POST':
        questions= request.POST.getlist('preguntas')
        answers= request.POST.getlist("respuestas")

    for q, a in zip(questions, answers):
        question= Question.objects.get(id=q)
        answer = Answer.objects.get(id=a)
        #intentos=+1
        userR=UserResponse.objects.create(user=user, quiz=quiz,  question=question, answer=answer)
        userR.save()
        #cat=userR.answer.learning_style
        #print(cat)######_-------------->ecluir informacion de clase
       
    return redirect('/')