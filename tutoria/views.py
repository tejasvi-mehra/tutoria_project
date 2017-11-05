from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Tutor, Student, Session
from django.db.models import Q
import datetime


""" functions to be imported """

def filter_sessions(sessions, days):
    time_delta = datetime.timedelta(days=days)
    tdy = datetime.datetime.today()
    week = tdy + time_delta
    final = []
    for sesh in sessions:
        if sesh.startTime > tdy and sesh.startTime < week:
            final.append(sesh)
    return final

def get_tutor_sessions(username):
    booked = []
    try:
        tutor = Tutor.objects.get(username = request.user.username)
        try:
            booked = tutor.session_set.all()
        except:
            booked = []
    except:
        booked = []
    return booked

def get_student_sessions(username):
    booked = []
    try:
        student = Student.objects.get(username = request.user.username)
        try:
            booked = student.session_set.all()
        except:
            booked = []
    except:
        booked = []
    return booked

def get_sessions(username):
    tutor_sessions = get_tutor_sessions(username)
    student_sessions = get_student_sessions(username)
    tutor_sessions = filter_sessions(tutor_sessions, 7)
    student_sessions = filter_sessions(student_sessions, 7)
    return (tutor_sessions, student_sessions)

def get_day(day):
    time_delta = datetime.timedelta(minutes=30)
    start_time = datetime.time(9,0,0,0)
    start = datetime.datetime.combine(day, start_time)
    day = []
    for i in range(0,16):
        day.append({
            'time' : start + time_delta*i,
            'status' : 'vacant'
        })
    return day

def create_week(days):
    time_delta = datetime.timedelta(days=1)
    start_date = datetime.datetime.today().date()
    week = []
    for i in range(0,days):
        week = week + get_day(start_date + i*time_delta)
    return week

def manage_sessions(all_sessions, week):
    for item in week:
        for sesh in all_sessions:
            if item.time == sesh.start_time:
                item.status = sesh.status
    return week

""" functions to be imported """

def home(request):
    return render(request, 'tutoria/home.html')

def dashboard(request):
    username = request.user.username
    tutor_sessions, student_sessions = get_sessions(username)
    context = {
        'name' : request.user.username,
        'tutor_sessions' : tutor_sessions,
        'student_sessions' : student_sessions
        'id' : request.user.id
    }
    return render(request, 'tutoria/dashboard.html', context)

def manage_student_time_table(request):
    username = request.user.username
    all_sessions = get_student_sessions(username)
    all_sessions = filter_sessions(all_sessions, 7)
    week = create_week(7)
    result = manage_sessions(all_sessions, week)
    return result

def manage_tutor_time_table(request):
    username = request.user.username
    all_sessions = get_student_sessions(username)
    all_sessions = filter_sessions(all_sessions, 14)
    week = create_week(all_sessions, 14)
    result = manage_sessions(all_sessions, week)
    return result

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
                isStudent = isStudent,
                rate = request.POST['rate'],
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

def lock(request, date_time, duration):
    sessions = get_tutor_sessions(request.user.username)
    flag = False
    for item in sessions:
        if item.start_time == date_time:
            flag = True
    if flag == True:
        session = Session(
            tutor = tutor,
            student = None,
            amount = 0,
            status = 'BLOCKED',
            start_time = date_time,
            duration = duration
        )
        session.save()
        return redirect('/tutoria/dashboard')
    else:
        return redirect('/tutoria/error')

def viewTimetable(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    sessions = filter_sessions(get_tutor_sessions(tutor.username), 7)
    context = {
        'tutor' : tutor,
        'sessions' : sessions
    }
    return render(request, 'tutoria/viewTimetable.html', context)

def check_conflict(tutor, student, date_time):
    if student.username == tutor.username:
        return False
    if date_time < datetime.datetime.today() + datetime.timedelta(hours=24):
        return False
    # one more condition to be checked....
    # dont allow student to book two sessions with same tutor on same day.
    tutor_sessions = filter_sessions(get_tutor_sessions(tutor.username), 7)
    student_sessions  = filter_sessions(get_student_sessions(student.username), 7)

    sessions = tutor_sessions + student_sessions
    for item in sessions:
        if item.start_time == date_time:
            return True
    return False

def book(request, tutor_id, date_time, duration):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        student = get_object_or_404(Student, username=request.user.username)
        if !check_conflict(tutor, student, date_time):
            session = Session(
                tutor = tutor,
                student = student,
                start_time = date_time,
                duration = duration
            )
            session.save()
            return redirect('/tutoria/dashboard')
        else:
            return redirect('/tutoria/error')
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
        if session.start_time < datetime.datetime.today() + datetime.timedelta(hours=24):
            return redirect('/tutoria/error')
        else:
            session.delete()
            return redirect('/tutoria/dashboard')
    else:
        context = {
            'date': date,
            'time': time,
            'tutor': session.tutor
        }
        return render(request, 'tutoria/cancelSession.html', context)
