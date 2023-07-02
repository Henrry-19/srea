from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.quiz.forms import*
from apps.quiz.models import *
from apps.srea.models import *
from apps.user.models import *
from apps.srea.mixins import*
from apps.srea.forms import*
from django.views.generic import* #importando la vista genérica
from collections import defaultdict
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from itertools import islice
from django.http import JsonResponse

class FileLoadedCreateView(CreateView):
    model = SubirArchivos
    form_class = SubirArchivoForms
    template_name = 'quiz/file/upload_quiz.html'
    success_url = reverse_lazy('apps.srea:p_asignatura')
    #permission_required = 'gestion_servicio.add_archivocargado'  # despues se le asigna este servicio
    

@login_required#Sirve
@permission_required('quiz.add_quiz')
def CargarQuiz(request,asignatura_id):#Vistas basadas en funciones
    form = FileUploadedForms(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('srea:registrar-quiz', asignatura_id=asignatura_id)
    else:
        form = FileUploadedForms()
    context={
        #'asignatura_id':asignatura_id,
        'asignatura_id':asignatura_id,
        'form':form,
    }
    return render(request, 'quiz/upload_quiz.html', context)

#@login_required#Sirve
#@permission_required('quiz.view_quiz')
class ListQuiz(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):#Presenta la lista de cuestionarios cargados
    model = Quiz
    template_name = 'quiz/list.html'
    permission_required='view_quiz'
    context_object_name  = 'quizzes'
    queryset = Quiz.objects.filter(state=True)


@login_required#Sirve
@permission_required('quiz.view_quiz')
def ListaQuizUsuario(request, asignatura_id, user_id):
    asig= get_object_or_404(Asignatura, id=asignatura_id)
    usu = get_object_or_404(User, id=user_id)

    user=request.user
    print('.....>',asig.docente)
    #print('.....>',user.groups.all())
#####################################################################>>>>>>>>>>>>>>>>>>>>

    context = {
		'asig': asig,
        'usu':usu,
	}
    return render(request,'quiz/list.html', context=context)


###############Editar Quiz#####################################
@login_required#Sirve
@permission_required('quiz.change_quiz')
def EditQuiz(request,asignatura_id, unidad_id, quiz_id):#Editar unidad
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = NewQuizForm(request.POST, request.FILES, instance=quiz)
            if form.is_valid():
                quiz.title = form.cleaned_data.get('title')
                quiz.description = form.cleaned_data.get('description')
                quiz.due=form.cleaned_data.get('due')
                quiz.allowed_attemps=form.cleaned_data.get('allowed_attemps')
                quiz.time_limit_mins=form.cleaned_data.get('time_limit_mins')
                quiz.save()
               
                return redirect('srea:take-quiz', asignatura_id=asignatura_id, unidad_id=unidad_id, quiz_id=quiz_id)
        else:
            form = NewQuizForm(instance=quiz)
    context = {
		'form': form,
		'quiz': quiz,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
        'url_list': reverse_lazy('srea:p_asignatura'),
	}
    return render(request, 'quiz/editquiz.html', context)


@login_required#Sirve
@permission_required('quiz.change_question')
def EditQuestion(request,asignatura_id, unidad_id, quiz_id, question_id):#Editar unidad
    question = get_object_or_404(Question, id=question_id)
    
    if request.user.is_staff:
        if request.method == 'POST':
            form = NewQuestionForm2(request.POST, request.FILES, instance=question)
            if form.is_valid():
                #question.question_text = form.cleaned_data.get('question_text')
                #answers=form.cleaned_data.get('answers')
                #resp=Answer.objects.filter(pk__in=answers)
                #print(resp)
                #question.answers.set(resp)
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
@login_required#Sirve
@permission_required('quiz.change_answer')
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


#############################04-06-2023#################################################

@login_required#Sirve
@permission_required('quiz.view_quiz')
def QuizDetail(request,asignatura_id, unidad_id,external_id):
    #user = request.user
    quiz=get_object_or_404(Quiz, id=external_id)
    #mis_intentos= Attempter.objects.filter(quiz=quiz, user=user)
    #print(quiz.external_id)
    context={
        'quiz':quiz,
        #'mis_intentos':mis_intentos,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id
    }

    return render(request, 'quiz/quizdetail.html', context)


@login_required#Sirve-->Con este método estoy listando las preguntas y respuestas del cuestionario
@permission_required('quiz.view_quiz')
def TakeQuiz(request,asignatura_id, unidad_id, quiz_id):#Tomar el cuestionario
    quiz=get_object_or_404(Quiz, id=quiz_id)
    questions=Question.objects.filter(quiz=quiz.id)

    context={
        'quiz':quiz,
        'question':questions,
        'asignatura_id':asignatura_id,
        'unidad_id':unidad_id,
    }
    
    return render(request, 'quiz/takequiz.html', context)
    
    


@login_required#Sirve-->Métdo usado para manejar el tiempo del quiz  en Js
@permission_required('quiz.view_quiz')
def TakeQuiz2(request,asignatura_id, unidad_id, quiz_id):#Tomar el cuestionario
    quiz=get_object_or_404(Quiz, id=quiz_id)
    #questions=Question.objects.filter(quiz=quiz.id)
    
    questions=[]
    for q in quiz.get_questions():
        answers=[]
        for a in q.get_answer():
            answers.append(a.text)

        questions.append({str(q): answers})

        
    return JsonResponse({
        'data': questions,
        'time': quiz.time_limit
    })


@login_required#sirve
@permission_required('quiz.view_quiz')
def SubmitAttempt(request,asignatura_id, unidad_id,quiz_id):#Envíar intento-->Podemos reutilizar este método
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
        #print("RESPUESTAS------>",cat)
    return redirect('srea:p_asignatura')


#Presentar todos los Quiz########
@login_required
@permission_required('quiz.view_quiz')
def presentarResultado(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    prueba_usuario=UserResponse.objects.filter(quiz=quiz)
    respuestas = []
    for p_u in prueba_usuario:
        respuestas.append(p_u.answer.learning_style) 

    recuentos = defaultdict(int)

    for categoria in respuestas:
        recuentos[categoria] += 1
    cat=[]
    contador=[]
    for categoria, count in recuentos.items():
        cat.append(categoria.name)
        contador.append(count)

    if 'N/a' in cat:
        posicion=cat.index("N/a")
        cat.remove("N/a")
        contador.pop(posicion)


    estilo_dominate_usuario=""
    if contador:
        estilo_dominante = max(contador, key=int)
        #print("---->",estilo_dominante)
        posicion_ed=contador.index(estilo_dominante)

        estilo_dominate_usuario=cat[posicion_ed]

    context = {
        'quiz': quiz,
        'estilos':cat,
        'count':contador,
        'estilo_dominate_usuario':estilo_dominate_usuario

    }
    return render(request,'attempter/attempter_resultado.html', context=context)

@login_required
@permission_required('quiz.view_quiz')
def presentarTodosResultado(request,asignatura_id):
    #user=request.user
    #usuario=UserResponse.objects.filter(user=user.id)
    lista = get_object_or_404(Asignatura, id=asignatura_id)
    #################################################################
    unique_sweets = []
    for u in lista.users.all():  
        filtrar=UserResponse.objects.filter(user=u)
        #print('---->',u)
        for usu in filtrar:
            unique_sweets.append(usu.user)
            #print(usu.user)
    #########OBtener valores únicos###########
    #print('---->',unique_sweets)
    valor_unico=set(unique_sweets)
    lista_valores_unicos=[]
    for n in valor_unico:
        lista_valores_unicos.append(n)
    #print("NN--->")
    total_usuarios=len(lista_valores_unicos)

    #############################################

    prueba_usuario=UserResponse.objects.all()
    #usuarios=UserResponse.objects.all()
    respuestas = []
    for p_u in prueba_usuario:
        respuestas.append(p_u.answer.learning_style)
    #numeros_unicos = list(set(numeros))
    recuentos = defaultdict(int)

    for categoria in respuestas:
        recuentos[categoria] += 1
    cat=[]
    contador=[]
    for categoria, count in recuentos.items():
        #print(f'{categoria}: {count}')
        cat.append(categoria.name)
        contador.append(count)


    if 'N/a' in cat:
        posicion=cat.index("N/a")
        cat.remove("N/a")
        contador.pop(posicion)


    estilo_dominate_usuario=""
    if contador:
        estilo_dominante = max(contador, key=int)
        #print("---->",estilo_dominante)
        posicion_ed=contador.index(estilo_dominante)

        estilo_dominate_usuario=cat[posicion_ed]
####################################################    
    request.user.get_group_session()
####################################################
    context = {
        'lista_valores_unicos':lista_valores_unicos,
        'total_usuarios':total_usuarios,
        'lista':lista,
        'estilos':cat,
        'count':contador,
        'estilo_dominate_usuario':estilo_dominate_usuario

    }

    return render(request,'quiz/resultado/resultado_u_quiz.html', context=context)

@login_required
@permission_required('quiz.view_quiz')
def presentarResultadoUsuario(request):
    user=request.user
    prueba_usuario=UserResponse.objects.filter(user=user)
    ###################FICHA########################
    ficha=[]
    if Ficha.objects.filter(user=user.id).exists():
        ficha.append(Ficha.objects.filter(user=user.id))
    else:        
        print("No existe una ficha")
    #print(ficha)
    ###############################################    

    respuestas = []
   
    for p_u in prueba_usuario:
        respuestas.append(p_u.answer.learning_style)



    recuentos = defaultdict(int)

    eliminar=[]
    for categoria in respuestas:
        eliminar.append(categoria)

    for categ in eliminar:
        recuentos[categ] += 1

    
    

    cat=[]
    contador=[]
    #print(recuentos)
    for categoria, count in recuentos.items():
        cat.append(categoria.name)
        contador.append(count)

    #print(cat)
    if 'N/a' in cat:
        posicion=cat.index("N/a")
        cat.remove("N/a")
        contador.pop(posicion)


    estilo_dominate_usuario=""
    if contador:
        estilo_dominante = max(contador, key=int)
        #print("---->",estilo_dominante)
        posicion_ed=contador.index(estilo_dominante)

        estilo_dominate_usuario=cat[posicion_ed]

####################################################    
    request.user.get_group_session()
####################################################
    context = {
        'user': user,
        'ficha': ficha,
        'estilos':cat,
        'count':contador,
        'estilo_dominate_usuario':estilo_dominate_usuario
    }

    return render(request,'index1.html', context=context)




@login_required
@permission_required('quiz.view_quiz')
def presentarResultadoUsuario2(request, user_id):
    user=User.objects.filter(id=user_id)
    
    ###################FICHA########################
    ficha=[]
    if Ficha.objects.filter(user=user_id).exists():
        ficha.append(Ficha.objects.filter(user=user_id))
    else:        
        print("No existe una ficha")
    #print(ficha)
    ###############################################

    prueba_usuario=UserResponse.objects.filter(user=user_id)
    respuestas = []
    for p_u in prueba_usuario:
        respuestas.append(p_u.answer.learning_style)
    
    recuentos = defaultdict(int)

    for categoria in respuestas:
        recuentos[categoria] += 1
    cat=[]
    contador=[]
    for categoria, count in recuentos.items():
        #print(f'{categoria}: {count}')
        cat.append(categoria.name)
        contador.append(count)
        
    #print(cat,"------",contador)
    if 'N/a' in cat:
        posicion=cat.index("N/a")
        cat.remove("N/a")
        contador.pop(posicion)


    estilo_dominate_usuario=""
    if contador:
        estilo_dominante = max(contador, key=int)
        #print("---->",estilo_dominante)
        posicion_ed=contador.index(estilo_dominante)

        estilo_dominate_usuario=cat[posicion_ed]

    context = {
        'user':user,
        'ficha':ficha,
        'estilos':cat,
        'count':contador,
        'estilo_dominate_usuario':estilo_dominate_usuario

    }

    return render(request,'quiz/resultado/resultado_particular.html', context=context)

@login_required
#@permission_required('quiz.view_quiz')
def presentarQuizDocente(request, asignatura_id):

    course=get_object_or_404(Asignatura, id=asignatura_id)
    
    context={
        'asignatura_id':asignatura_id,
        'course':course,
        'title': "Evaluación docente",
        'modelo':'Evaluación',
        'date_now':datetime.now()


    }

    return render(request, 'user_quiz/docente_quiz.html', context)
