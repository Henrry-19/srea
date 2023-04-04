from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.quiz.forms import*
from apps.quiz.models import *
from apps.srea.models import *
from apps.srea.mixins import*
from django.views.generic import* #importando la vista genérica

from django.contrib.auth.decorators import permission_required
# Create your views here.
@login_required
@permission_required('quizzes.add_quizzes')
def NewQuiz(request,asignatura_id, unidad_id):#Vistas basadas en funciones
    user = request.user
    unidad=get_object_or_404(Unidad, id=unidad_id)
    if request.method=='POST':
        form = NewQuizForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            due = form.cleaned_data.get('due')
            allowed_attemps = form.cleaned_data.get('allowed_attemps')
            time_limit_mins = form.cleaned_data.get('time_limit_mins')
            quiz = Quizzes.objects.create(user=user,title=title,description=description,due=due,allowed_attemps=allowed_attemps,time_limit_mins=time_limit_mins)
            unidad.cuestionario.add(quiz)
            unidad.save()
            return redirect('srea:new-question', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz.id)
    else:
        form = NewQuizForm
    context={
        'form':form,

    }
    return render(request, 'quiz/newquiz.html', context)


@login_required
@permission_required('question.add_question')
def NewQuestion(request, asignatura_id, unidad_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    if request.method == 'POST':
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                    question_text = form.cleaned_data.get('question_text')
                    points = form.cleaned_data.get('points')
                    answer_text = request.POST.getlist('answer_text')
                    is_correct = request.POST.getlist('is_correct')
                    #print(is_correct , '------>')
                    #print(is_correct)
                    question= Question.objects.create(question_text=question_text, user=user, points=points)
                    for a, c in zip(answer_text, is_correct):
                        answer = Answer.objects.create(answer_text=a, is_correct=c, user=user)
                        question.answers.add(answer)
                        #print(question)
                        question.save()
                        quiz.questions.add(question)
                        quiz.save()
                        #print(contador , 'toby')
                    return redirect('srea:new-question', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz.id)
    else:
            form = NewQuestionForm()
   
    context={
         
            'form':form,
            

    }

    return render(request,'quiz/newquestion.html', context)
@login_required
def QuizDetail(request,asignatura_id, unidad_id,quiz_id):
    user = request.user
    quiz=get_object_or_404(Quizzes, id=quiz_id)
    mis_intentos= Attempter.objects.filter(quiz=quiz, user=user)

    context={
        'quiz':quiz,
        'mis_intentos':mis_intentos,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id
    }

    return render(request, 'quiz/quizdetail.html', context)
@login_required
def TakeQuiz(request,asignatura_id, unidad_id, quiz_id):
    quiz=get_object_or_404(Quizzes, id=quiz_id)

    context={
        'quiz':quiz,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
    }

    return render(request, 'quiz/takequiz.html', context)
@login_required
def SubmitAttempt(request,asignatura_id, unidad_id,quiz_id):#Envíar intento
    user=request.user
    quiz=get_object_or_404(Quizzes, id=quiz_id)
    puntos_ganados= 0
    if request.method=='POST':
        questions=request.POST.getlist('questions')
        answers = request.POST.getlist('answer')
        attempter=Attempter.objects.create(user=user, quiz=quiz, score=0)

    for q, a in zip(questions, answers):
        question= Question.objects.get(id=q)
        answer = Answer.objects.get(id=a)

        Attempt.objects.create(quiz=quiz, attempter=attempter, questions=question, answer=answer)
        if answer.is_correct==True:
            puntos_ganados += question.points
            attempter.score += puntos_ganados
            attempter.save()
    return redirect('srea:p_asignatura')
     
@login_required
def AttemptDetail(request,asignatura_id, unidad_id,quiz_id, attempt_id):#Resultado
    user=request.user
    quiz=get_object_or_404(Quizzes, id=quiz_id)
    attempts= Attempt.objects.filter(quiz=quiz, attempter__user=user)
    print(attempts)
    context = {
        'quiz':quiz,
        'attempts':attempts,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'attempt':attempt_id
    }

    return render(request, 'quiz/attemptdetail.html', context)


    
