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
def NewQuiz1(request,asignatura_id, unidad_id):#Vistas basadas en funciones
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

##########################################Doble---Quiz##################################################33
@login_required
@permission_required('quizzes.add_quizzes')
def NewQuiz(request,asignatura_id, unidad_id):#Vistas basadas en funciones
    #user = request.user
    unidad=get_object_or_404(Unidad, id=unidad_id)
    if request.method=='POST':
        form = NewQuizForm(request.POST)
        if form.is_valid():
            cat = form.cleaned_data.get('cat')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            due = form.cleaned_data.get('due')
            allowed_attemps = form.cleaned_data.get('allowed_attemps')
            time_limit_mins = form.cleaned_data.get('time_limit_mins')
            quiz = Quizzes.objects.create(cat=cat,title=title,description=description,due=due,allowed_attemps=allowed_attemps,time_limit_mins=time_limit_mins)
            
            unidad.cuestionario.add(quiz)
            unidad.save()
            return redirect('srea:new-question', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz.id)
        #print(form)
    else:
        form = NewQuizForm
    context={
        'asignatura_id':asignatura_id,
        'form':form,
    }
    return render(request, 'quiz/newquiz.html', context)

###############Editar Quiz#####################################
@login_required
@permission_required('quiz.change_quiz')
def EditQuiz(request,asignatura_id, unidad_id, quiz_id):#Editar unidad
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = NewQuizForm2(request.POST, request.FILES, instance=quiz)
            if form.is_valid():
                quiz.title = form.cleaned_data.get('title')
                quiz.description = form.cleaned_data.get('description')
                quiz.due=form.cleaned_data.get('due')
                quiz.allowed_attemps=form.cleaned_data.get('allowed_attemps')
                quiz.time_limit_mins=form.cleaned_data.get('time_limit_mins')
                quiz.save()
               
                return redirect('srea:take-quiz', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz_id)
        else:
            form = NewQuizForm2(instance=quiz)
    context = {
		'form': form,
		'quiz': quiz,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'quiz/editquiz.html', context)


@login_required
@permission_required('question.add_question')
def NewQuestion(request, asignatura_id, unidad_id, quiz_id):
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    #print(quiz.cat, 'hola mundo')
    cat=ItemCat.objects.filter(cat=quiz.cat.id)
    
    if request.method == 'POST':
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                    question_text = form.cleaned_data.get('question_text')
                    answer_text = request.POST.getlist('answer_text')
                    respuesta = request.POST.getlist('respuesta')
                    question= Question.objects.create(question_text=question_text)
                    for a, c in zip(answer_text, respuesta):
                        answer = Answer.objects.create(answer_text=a, respuesta=c)
                        question.answers.add(answer)
                        question.save()
                        quiz.questions.add(question)
                        quiz.save()
                    return redirect('srea:new-question', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz.id)
    else:
            form = NewQuestionForm()
   
    context={
            'quiz_id':quiz_id,
            'unidad_id':unidad_id,
            'asignatura_id':asignatura_id,
            'form':form,
            'cat':cat
    }

    return render(request,'quiz/newquestion.html', context)

###############Actualizar-Preguntas##########################
@login_required
@permission_required('question.change_question')
def EditQuestion(request,asignatura_id, unidad_id, quiz_id, question_id):#Editar unidad
    question = get_object_or_404(Question, id=question_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = NewQuestionForm2(request.POST, request.FILES, instance=question)
            if form.is_valid():
                question.question_text = form.cleaned_data.get('question_text')
                answers=form.cleaned_data.get('answers')
                resp=Answer.objects.filter(pk__in=answers)
                #print(resp)
                question.answers.set(resp)
                question.save()
               
                return redirect('srea:take-quiz', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz_id)
        else:
            form = NewQuestionForm2(instance=question)
    context = {
		'form': form,
		'question': question,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'quiz_id':quiz_id,
        #'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'quiz/editquestion.html', context)


###############Actualizar-Respuestas##########################
@login_required
@permission_required('answer.change_answer')
def EditAnswer(request,asignatura_id, unidad_id, quiz_id,question_id, answer_id):#Editar unidad
    answer = get_object_or_404(Answer, id=answer_id)
    #print(answer)
    if request.user.is_staff:
        if request.method == 'POST':
            form = NewAnswerForm(request.POST, request.FILES, instance=answer)
            if form.is_valid():
                answer.answer_text = form.cleaned_data.get('answer_text')
                answer.respuesta=form.cleaned_data.get('respuesta')
                answer.save()
               
                return redirect('srea:take-quiz', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz_id)
        else:
            form = NewAnswerForm(instance=answer)
    context = {
		'form': form,
		'answer': answer,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'quiz_id':quiz_id,
        #'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'quiz/editanswer.html', context)


##############################################################################

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
def TakeQuiz(request,asignatura_id, unidad_id, quiz_id):#Tomar el cuestionario
    quiz=get_object_or_404(Quizzes, id=quiz_id)
    print(quiz.questions)
    context={
        'quiz':quiz,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
    }

    return render(request, 'quiz/takequiz.html', context)
@login_required
def SubmitAttempt(request,asignatura_id, unidad_id,quiz_id):#Envíar intento
    quiz=get_object_or_404(Quizzes, id=quiz_id)
    cat=ItemCat.objects.filter(cat=quiz.cat.id)
    puntos_ganados= 0
    ############VAK###################
    visual = 0
    auditivo=0
    kinestesico=0
    ###########CHAEA####################
    activo=0
    reflexivo=0
    teorico=0
    pragmatico=0
    ###################################
    user=request.user
    if request.method=='POST':
        questions= request.POST.getlist('question')
        answers= request.POST.getlist('answer')
        attempter=Attempter.objects.create(user=user, quiz=quiz, score=0)
    #print(cat, 'catt')
    estilos=[]
    
    for q, a in zip(questions, answers):
        question= Question.objects.get(id=q)
        answer = Answer.objects.get(id=a)

        Attempt.objects.create(attempter=attempter, answer=answer)#Contestar-->Guardar preguntas-respuestas
        #Completion.objects.create(user=user, asignatura_id=asignatura_id, quiz=quiz)
        
        indices=[cat[index] for index, elemento in enumerate(cat) if elemento.id==answer.respuesta]#index-->posición
        
        #num_apariciones = [(num.nombreItem,indices.count(num)) for num in set(indices)]
        num_apariciones = [(num.nombreItem) for num in set(indices)]
        estilos.append(num_apariciones)
       
        for nume in num_apariciones:
            if nume=='Visual':
                visual+=1
    #attempter.score = visual
        for a in num_apariciones:
            if a=='Auditivo':
                auditivo+=1

        for k in num_apariciones:
            if k=='Kinéstesico':
                kinestesico+=1

        for ac in num_apariciones:
            if ac=='activo':
                activo+=1
        for r in num_apariciones:
            if r=='reflexivo':
                reflexivo+=1 

        for t in num_apariciones:
            if t=='teórico':
                teorico+=1 

        for p in num_apariciones:
            if p=='pragmático':
                pragmatico+=1      
    print('Activo:',activo, 'Reflexivo: ', reflexivo, 'Teórico: ', teorico, 'Pragmático: ', pragmatico)
    #print('Visual:', visual, 'Auditivo: ', auditivo, 'Kinestésico:', kinestesico)
        


        #filtrar con el set
        #Sumando cada item
        #Prueba con más preguntas
        #Revisar como funciona el index, el nuevo for
          
            #puntos_ganados += question.points
            #attempter.score += puntos_ganados
            #attempter.save()
      
    return redirect('srea:p_asignatura')
     
@login_required
def AttemptDetail(request,asignatura_id, unidad_id,quiz_id, attempt_id):#Resultado
    user=request.user
    quiz=get_object_or_404(Quizzes, id=quiz_id)
    attempts= Attempt.objects.filter(attempter__user=user) ## Conectamos con attempter(mis intentos + user)
    
    context = {
        'quiz':quiz,
        'attempts':attempts,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'attempt':attempt_id
    }

    return render(request, 'quiz/attemptdetail.html', context)


    
