from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Note
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError

# Create your views here.


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    return render(request, 'Home.html')

def login_usr(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        usr = authenticate(request=request, username=username, password=passwd)
        if usr:
            login(request, usr)
            return redirect('/notes')
        else:
            return render(request, 'Login.html', {'invalid_user': True})

    return render(request, 'Login.html', {'invalid_user': False})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        if User.objects.filter(username=username).exists():
            return render(request, 'Register.html', {'error': 'Username already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'Register.html', {'error': 'Email already registered'})

        try:
            usr = User.objects.create_user(username=username, email=email, password=passwd)
            usr.save()
            return redirect('/login')

        except IntegrityError:
            return render(request, 'Register.html', {'error': 'Something went wrong. Try again.'})

    return render(request, 'Register.html')

@login_required(login_url='/login')
def note_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        note_obj = Note(title=title, content=content, user=request.user)
        note_obj.save()
        notes = Note.objects.filter(user = request.user).order_by('-created_at')
        return redirect('/notes')
    notes = Note.objects.filter(user = request.user).order_by('-created_at')
    for note in notes:
        note.local_created_at = timezone.localtime(note.created_at)
        print(note.local_created_at)
    return render(request, 'Notelist.html', {'notes': notes})

@login_required(login_url='/login')
def delete(request, id):
    note_obj = get_object_or_404(Note, id=id, user=request.user)
    if request.method == 'POST':
        note_obj.delete()
    return redirect('/notes')

@login_required(login_url='/login')
def edit(request, id):
    note_obj = get_object_or_404(Note, id=id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        note_obj.title = title
        note_obj.content = content
        note_obj.save()
    return redirect('/notes')

@login_required(login_url='/login')
def signout(request):
    logout(request)
    return redirect('/login')
