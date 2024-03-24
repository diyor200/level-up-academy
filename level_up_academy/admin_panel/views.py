from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def login_user(request):
    login_error = False
    if request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username,  password=password)
        if user:
            login(request, user)
            return redirect('dash')
        else:
            login_error = "Incorrect username or password. Please try again."
    return render(request, 'login.html', {"login_error": login_error})

@login_required(login_url='login')
def create_word(request):
    books = models.Book.objects.all()
    if request.method == "POST":
        book = request.POST['book']
        book_id = models.Book.objects.get(title = book).id
        return redirect ('dash2', book_id)
    context = {
        'books':books,
        'data':1
    }
    return render(request, "index.html", context)

@login_required(login_url='login')
def create_word2(request, id):
    unit = models.Unit.objects.filter(book_id = id)
    if request.method == "POST":
        unit = request.POST['unit']
        unit_id = models.Unit.objects.get(title = unit).id
        return redirect ('dash3', unit_id)
    return render(request, 'index.html', {'unit':unit, 'data':2})

@login_required(login_url='login')
def create_word3(request, id):
    passage = models.Passage.objects.filter(unit_id = id)
    if request.method == "POST":
        passage = request.POST['passage']
        passage_id = models.Passage.objects.get(title = passage).id
        return redirect ('dash4', passage_id)
    return render(request, 'index.html', {'passage':passage, 'data':3})

@login_required(login_url='login')
def word_finish(request, id):
    passage = models.Passage.objects.get(id = id)
    if request.method == "POST":
        word = request.POST['word']
        definition = request.POST['def']
        translated = request.POST['translated']
        models.Vocabulary.objects.create(
            book = passage.book,
            unit = passage.unit,
            passage = passage,
            word = word,
            definition = definition,
            translated = translated
        )
        if 'exit' in request.POST:
            return redirect('dash')
    return render(request, 'index.html', {'passage':passage, 'data':4})