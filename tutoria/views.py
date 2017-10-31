from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Tutor, Student, Session
from django.db.models import Q


sessionList = [
    ['09/01', '10:00'], ['09/01', '11:00'], ['09/01', '12:00'],
    ['09/01', '13:00'], ['09/01', '14:00'], ['09/01', '15:00'],
    ['09/01', '16:00'], ['09/01', '17:00'], ['09/02', '10:00'],
    ['09/03', '11:00']
]

def home(request):
    return render(request, 'tutoria/home.html')

def dashboard(request):
    booked = []
    try:
        student = Student.objects.get(username = request.user.username)
        print(student)
        booked = student.session_set.all()
        print("here", booked)
    except:
        tutor = Tutor.objects.get(username = request.user.username)
        try:
            booked = tutor.session_set.all()
        except:
            booked = []
    context = {
        'name' : request.user.username,
        'booked' : booked,
        'id' : request.user.id
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
    return render(request, 'tutoria/viewProfile.html', {'tutor':tutor})

def getSessions(sessions):
    booked = []
    for sesh in sessions:
        temp = [sesh.date, sesh.time]
        booked.append(temp)
    result = []
    for sesh in sessionList:
        temp = {'date' : sesh[0], 'time' : sesh[1], 'status' : False}
        if sesh in booked:
            temp.status = True
        result.append(temp)
    return result

def viewTimetable(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    sessions = tutor.session_set.all()
    result = getSessions(sessions)
    context = {
        'tutor' : tutor,
        'sessions' : result
    }
    return render(request, 'tutoria/viewTimetable.html', context)

def book(request, tutor_id, date, time):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        student = get_object_or_404(Student, username=request.user.username)
        session = Session(
            tutor = tutor,
            student = student,
            date = date,
            time = time
        )
        session.save()
        return redirect('/tutoria/dashboard')
    else:
        context = {
            'date': date,
            'time': time,
            'tutor': tutor
        }
        return render(request, 'tutoria/bookSession.html', context)

def cancel(request, date, time):
    student = Student.objects.get(username = request.user.username)
    session = Session.objects.get(student = student, date = date, time = time)
    if request.method == 'POST':
        session.delete()
        return redirect('/tutoria/dashboard')
    else:
        context = {
            'date': date,
            'time': time,
            'tutor': session.tutor
        }
        return render(request, 'tutoria/cancelSession.html', context)
