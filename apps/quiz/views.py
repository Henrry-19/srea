from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apps.quiz.forms import*
from apps.quiz.models import *

# Create your views here.

def NewQuiz(request, module_id):
    user = request.user
    
