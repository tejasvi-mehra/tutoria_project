from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Tutor, Student, Session, Transaction, AdminWallet
from django.db.models import Q
import datetime
from dateutil import parser

""" functions to be imported """

# filter the sessions array based on number of days
# looking forward
def filter_sessions(sessions, days):
    time_delta = datetime.timedelta(days=days)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    week = tdy + time_delta
    final = []
    for sesh in sessions:
        if sesh.start_time >= tdy and sesh.start_time < week:
            final.append(sesh)
    return final

# get tutor sessions which can be BOOKED or BLOCKED
def get_tutor_sessions(username):
    booked = []
    try:
        tutor = Tutor.objects.get(username=username)
        try:
            booked = tutor.session_set.all()
            print("booked", booked)
        except:
            booked = []
    except:
        booked = []
    return booked

# get student sessions which can be BOOKED
def get_student_sessions(username):
    # print("in get sessions", username)
    booked = []
    try:
        student = Student.objects.get(username=username)
        try:
            # print(student)
            booked = student.session_set.all()
            # print(booked[0])
        except:
            booked = []
    except:
        booked = []
    return booked

# look at function and understand
def get_sessions(username):
    tutor_sessions = get_tutor_sessions(username)
    student_sessions = get_student_sessions(username)
    # print(tutor_sessions, student_sessions)
    tutor_sessions = filter_sessions(tutor_sessions, 7)
    student_sessions = filter_sessions(student_sessions, 7)
    return (tutor_sessions, student_sessions)

# create day array -> has 16 objects, day is starting date
def get_day(day, minutes):
    time_delta = datetime.timedelta(minutes=minutes)
    start_time = datetime.time(9,0,0,0)
    start = datetime.datetime.combine(day, start_time)
    day = []
    slots = 8 if minutes == 60 else 16
    for i in range(0,slots):
        day.append({
            'time' : start + time_delta*i,
            'status' : 'vacant'
        })
    return day

# create week array -> days is number of days you want -> array of  days*16 objects
def create_week(days, minutes):
    time_delta = datetime.timedelta(days=1)
    start_date = datetime.datetime.today().date() + time_delta
    week = []
    for i in range(0,days):
        week = week + get_day(start_date + i*time_delta, minutes)
    return week

# modifies the wee array according to all_sessions
def manage_sessions(all_sessions, week):
    for item in week:
        for sesh in all_sessions:
            if item['time'] == sesh.start_time:
                item['status'] = sesh.status
    return week

# check if tutor or student
def check_person(username):
    try:
        student = Student.objects.get(username=username)
        if student.isTutor:
            return student, Tutor.objects.get(username=username)
        else:
            return student, False
    except:
            return False, Tutor.objects.get(username=username)

# return the balance of student or tutor
def get_balance(username):
    try:
        student = Student.objects.get(username=username)
        if student.isTutor:
            tutor = Tutor.objects.get(username=username)
            return tutor.balance
        else:
            return student.balance
    except:
        tutor = Tutor.objects.get(username=username)
        return tutor.balance

# Transfer money from student to admin on every booking
def sendFundsToAdmin(username, amount):
    student = Student.objects.get(username = username)
    if student.isTutor:
        tutor = Tutor.objects.get(username=username)
        tutor.balance= float(tutor.balance) - amount
        tutor.save()
    else:
        student.balance= float(student.balance) - amount
        student.save()
    admin = AdminWallet.objects.get(username = "admin")
    admin.amount = float(admin.amount) + amount
    admin.save()

# Refund money back to student
def refundFromAdmin(username, amount):
    student = Student.objects.get(username = username)
    if student.isTutor:
        tutor = Tutor.objects.get(username=username)
        tutor.balance = float(tutor.balance) + float(amount)
        tutor.save()
    else:
        student.balance= float(student.balance) + float(amount)
        student.save()
    admin = AdminWallet.objects.get(username = "admin")
    admin.amount = float(admin.amount) - float(amount)
    admin.save()

# Get transactions made in past 30 days
def get_transactions_outgoing(username):
    booked = []
    try:
        student = Student.objects.get(username=username)
        try:
            # print(student)
            booked = student.transaction_set.all()
            booked = filter_sessions(booked,30)
            # print(booked[0])
        except:
            booked = []
    except:
        booked = []

    return booked

# Get incoming transactios for past 30 days
""" functions to be imported """
def get_transactions_incoming(username):
    booked = []
    try:
        tutor = Tutor.objects.get(username=username)
        try:
            # print(student)
            booked = tutor.transaction_set.all()
            booked = filter_sessions(booked,30)
            # print(booked[0])
        except:
            booked = []
    except:
        booked = []

    return booked

def home(request):
    return render(request, 'tutoria/home.html')

def dashboard(request):
    username = request.user.username
    tutor_sessions, student_sessions = get_sessions(username)
    student, tutor = check_person(username)
    balance = get_balance(username)
    transactions_outgoing = get_transactions_outgoing(username)
    transactions_incoming = get_transactions_incoming(username)
    context = {
        'name' : request.user.username,
        'tutor_sessions' : tutor_sessions,
        'student_sessions' : student_sessions,
        'student' : student,
        'tutor': tutor,
        'balance': balance,
        'transactions_outgoing' : transactions_outgoing,
        'transactions_incoming' : transactions_incoming
    }
    return render(request, 'tutoria/dashboard.html', context)

def manage_student_time_table(request):
    username = request.user.username
    all_sessions = get_student_sessions(username)
    all_sessions = filter_sessions(all_sessions, 7)
    week = create_week(7, 30)
    result = manage_sessions(all_sessions, week)
    return render(request, 'tutoria/mstt.html', {'sessions' : result})

def manage_tutor_time_table(request):
    username = request.user.username
    all_sessions = get_tutor_sessions(username)
    all_sessions = filter_sessions(all_sessions, 14)
    tutor = Tutor.objects.get(username=username)
    week = create_week(14, 60) if tutor.tutortype == 'private' else create_week(14, 30)
    result = manage_sessions(all_sessions, week)
    return render(request, 'tutoria/mttt.html', {'sessions' : result})

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

def set_profile(request):
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

def tutor_name_search(request):
    if request.method == 'POST':
        field = request.POST['nameSearch']
        tutors = Tutor.objects.filter(username__startswith=field)
        return render(request, 'tutoria/search.html', {'tutors': tutors})

def view_tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    return render(request, 'tutoria/viewProfile.html', {'tutor':tutor})

def tutor_lock_session(request, date_time):
    tolock = parser.parse(date_time)
    tutor = Tutor.objects.get(username=request.user.username)
    td = datetime.timedelta(minutes=60) if tutor.tutortype == 'private' else datetime.timedelta(minutes=30)
    duration = 60 if tutor.tutortype == 'private' else 30
    sessions = get_tutor_sessions(request.user.username)
    flag = False
    for item in sessions:
        if item.start_time == tolock:
            flag = True
    if flag == False:
        session = Session(
            tutor = tutor,
            student = None,
            amount = 0,
            status = 'BLOCKED',
            start_time = tolock,
            end_time = tolock + td,
            duration = duration
        )
        session.save()
        return redirect('/tutoria/dashboard')
    else:
        return render(request, 'tutoria/mttt.html', {'error' : 'cant lock already been booked'})

def view_tutor_timetable(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    sessions = filter_sessions(get_tutor_sessions(tutor.username), 7)
    print(sessions)
    week = create_week(7, 60) if tutor.tutortype == 'private' else create_week(7, 30)
    result = manage_sessions(sessions, week)
    # print(result)
    context = {
        'tutor' : tutor,
        'sessions' : result
    }
    return render(request, 'tutoria/viewTimetable.html', context)

# one more condition to be checked....
# dont allow student to book two sessions with same tutor on same day.
def check_conflict(tutor, student, date_time):
    # print(date_time, datetime.datetime.today(), datetime.timedelta(hours=24))
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    print(date_time < datetime.datetime.today() + datetime.timedelta(hours=24))
    if student.username == tutor.username:
        return False
    if date_time < tdy + datetime.timedelta(hours=24):
        return False
    tutor_sessions = filter_sessions(get_tutor_sessions(tutor.username), 7)
    student_sessions  = filter_sessions(get_student_sessions(student.username), 7)
    sessions = tutor_sessions + student_sessions
    for item in sessions:
        if item.start_time <= date_time and date_time < item.end_time:
            return False
    return True

def book(request, tutor_id, date_time):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    start_time = parser.parse(date_time)
    if request.method == 'POST':
        student = get_object_or_404(Student, username=request.user.username)
        if check_conflict(tutor, student, start_time):
            duration = 60 if tutor.tutortype == 'private' else 30
            td = datetime.timedelta(minutes=60) if tutor.tutortype == 'private' else datetime.timedelta(minutes=30)
            #  Deduct from wallet

            costOfBooking = (float(tutor.rate) + float(tutor.rate)*0.05) if tutor.tutortype == 'private' else 0
            if costOfBooking > student.balance :
                return render(request, 'tutoria/bookSession.html', {'error' : 'Insufficient Funds !!.'})
            else:
                session = Session(
                tutor = tutor,
                student = student,
                start_time = start_time,
                end_time = start_time + td,
                duration = duration,
                amount = tutor.rate,
                status = 'BOOKED'
                )
                session.save()
                commission= float(tutor.rate)*0.05
                transaction = Transaction(
                tutor = tutor,
                student = student,
                start_time = start_time,
                end_time = start_time + td,
                amount = float(tutor.rate),
                commission = commission
                )
                transaction.save()
                sendFundsToAdmin(student.username, costOfBooking)
                return redirect('/tutoria/dashboard')
        else:
            return render(request, 'tutoria/bookSession.html', {'error' : 'conflict with another booked slot.'})
    else:
        context = {
            'date': date_time,
            'tutor': tutor
        }
        return render(request, 'tutoria/bookSession.html', context)

def detail_cancel(request, date_time):
    tocancel = parser.parse(date_time)
    student = Student.objects.get(username = request.user.username)
    session = Session.objects.get(student = student, start_time=tocancel)
    transaction =Transaction.objects.get(student = student, start_time = tocancel)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    if request.method == 'POST':
        if session.start_time < tdy + datetime.timedelta(hours=24):
            return redirect('/tutoria/session_detail.html', {'error': 'can\'t cancel'})
        else:
            # refund and delete transaction
            refund_amount = transaction.amount + transaction.commission
            refundFromAdmin(student.username, refund_amount)
            session.delete()
            transaction.delete()
            return redirect('/tutoria/dashboard')
    else:
        context = {
            'tutor' : session.tutor,
            'start' : session.start_time,
            'end' : session.end_time,
            'duration': session.duration
        }
        return render(request, 'tutoria/session_detail.html', context)

def add_funds(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        student = Student.objects.get(username = request.user.username)
        if student.isTutor:
            tutor = Tutor.objects.get(username=request.user.username)
            tutor.balance = float(tutor.balance) + float(amount)
            tutor.save()
        else:
            student.balance= float(student.balance) + float(amount)
            student.save()
        return redirect('/tutoria/dashboard')
    else:
        return render(request, 'tutoria/add_funds.html')
