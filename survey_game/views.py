from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти.')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    polls = Poll.objects.all()
    return render(request, 'Home.html', {'polls': polls})

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = Question.objects.filter(poll_id=poll_id)

    user_answers = UserAnswer.objects.filter(
        user=request.user,
        question__poll_id=poll_id  # Фильтруем по poll_id через связь с Question
    )

    if user_answers:
        return redirect('results', poll_id = poll_id)

    if request.method == 'POST':
        for question in questions:
            rating = request.POST.get(f"rating_{question.id}")
            if rating:
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'rating': int(rating)}
                )
        return redirect('results', poll_id = poll_id)

    return render(request, 'Vote.html', {'poll': poll, 'questions': questions})

@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll_questions = Question.objects.filter(poll_id = poll_id)
    user_answers = UserAnswer.objects.filter(
        user=request.user,
        question__poll_id=poll_id  # Фильтруем по poll_id через связь с Question
    )
    avg_scores = []

    for q in poll_questions:
        answers = UserAnswer.objects.filter(question=q)
        if answers.exists():
            avg = round(sum(a.rating for a in answers) / answers.count(), 2)
        else:
            avg = 'Нет данных'
        avg_scores.append((q.text, avg))

    return render(request, 'results.html', context={"poll": poll, "user_answers":user_answers, "avg_scores":avg_scores})

@login_required
def create(request):
    if request.method == 'POST':
        poll_name = request.POST.get('poll_name')

        # Создаем опрос
        poll = Poll.objects.create(name=poll_name)

        # Собираем все вопросы
        for key, value in request.POST.items():
            if key.startswith('question_'):
                Question.objects.create(text=value, poll=poll)

        return redirect('home')


    return render(request, 'create.html')
