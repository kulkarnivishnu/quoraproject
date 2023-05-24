# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Question, Answer

def home(request):
    return HttpResponse('Welcome to Quora')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('questions')
    return render(request, 'quora/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'quora/register.html')

@login_required
def questions(request):
    questions = Question.objects.all()
    return render(request, 'quora/questions.html', {'questions': questions})

@login_required
def question_detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        answers = question.answer_set.all()
        return render(request, 'quora/question_detail.html', {'question': question, 'answers': answers})
    except Question.DoesNotExist:
        return HttpResponse('Question does not exist')

@login_required
def answer_question(request, question_id):
    if request.method == 'POST':
        try:
            question = Question.objects.get(id=question_id)
            content = request.POST.get('content')
            answer = Answer.objects.create(content=content, author=request.user, question=question)
            return redirect('question_detail', question_id=question_id)
        except Question.DoesNotExist:
            return HttpResponse('Question does not exist')
    return render(request, 'quora/answer_question.html', {'question_id': question_id})

@login_required
def like_answer(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        answer.likes.add(request.user)
        return redirect('question_detail', question_id=answer.question.id)
    except Answer.DoesNotExist:
        return HttpResponse('Answer does not exist')
