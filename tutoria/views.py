from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Tutor, Student, Session
from django.db.models import Q

def home(request):
    return render(request, 'tutoria/home.html')

def dashboard(request):
    user = request.user.username

    context = {
        'name' : request.user.username,
        
    }
    return render(request, 'tutoria/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/tutoria/setProfile/')
    else:
        form = RegisterForm()
    return render(request, 'tutoria/register.html', {'form' : form})

def setProfile(request):
    if request.method == 'POST':
        temp = request.POST.getlist('checks')
        isTutor = False
        isStudent = False
        if 'student' in temp:
            isStudent = True
        if 'tutor' in temp:
            isTutor = True
        if temp[0] == 'tutor':
            tutor = Tutor(
                name = request.user.first_name + request.user.last_name,
                username = request.user.username,
                biography = request.POST['biography'],
                university = request.POST['university'],
                tutortype = temp[1],
                balance = request.POST['balance'],
                isStudent = isStudent
            )
            tutor.save()
        if 'student' in temp:
            student = Student(
                name = request.user.first_name + request.user.last_name,
                username = request.user.username,
                balance = request.POST['balance'],
                isTutor = isTutor
            )
            student.save()
        return redirect('/tutoria/dashboard')
    return render(request, 'tutoria/setProfile.html')

def search(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutoria/search.html', {'tutors': tutors})

def nameSearch(request):
    if request.method == 'POST':
        field = request.POST['nameSearch']
        tutors = Tutor.objects.filter(username__startswith=field)
        return render(request, 'tutoria/search.html', {'tutors': tutors})

def viewProfile(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    # data = getData(tutor.sessionInfo)
    # search for user in database
    # get sessions from user.sessionInfo
    # call method and fix data
    # send data in context.sessions.
    return render(request, 'tutoria/viewProfile.html', {'tutor':tutor})

def book(request, tutor_id):
    if request.method == 'POST':
        a = 1
    # create session model save it and redirect to dashboard.
    # in dashboard create a booked session section where you can query the
    # session model and if it matches the user then display it.
    else:
        a = 2
    # display the time table of the tutor using tutor_id.
    # we query the session model, you send to front end and render
    # for each time slot you check if back end has sent something
    # if not booked then render as available.
