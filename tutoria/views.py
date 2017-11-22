from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Tutor, Student, Session, Transaction, MyTutorsWallet, Notification, Review, Wallet, Coupon
from django.db.models import Q
import datetime
from dateutil import parser
from datetime import date
import time as ttime
from django.core.files.storage import FileSystemStorage, Storage
from django.http import JsonResponse

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
        booked = tutor.session_set.all()
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
    # try:
    #     student = Student.objects.get(username=username)
    #     if student.isTutor:
    #         tutor = Tutor.objects.get(username=username)
    #         return tutor.balance
    #     else:
    #         return student.balance
    # except:
    #     tutor = Tutor.objects.get(username=username)
    #     return tutor.balance

    wallet = Wallet.objects.get(username=username)
    return wallet.balance;

# Transfer money from student to admin on every booking
def sendFundsToAdmin(username, amount):
    # student = Student.objects.get(username = username)
    # if student.isTutor:
    #     tutor = Tutor.objects.get(username=username)
    #     tutor.balance= float(tutor.balance) - amount
    #     tutor.save()
    # else:
    #     student.balance= float(student.balance) - amount
    #     student.save()

    wallet = Wallet.objects.get(username=username)
    wallet.balance = float(wallet.balance)-amount
    wallet.save()
    admin = MyTutorsWallet.objects.get(username = "mytutors")
    admin.amount = float(admin.amount) + amount
    admin.save()

# Refund money back to student
def refundFromAdmin(username, amount):
    # student = Student.objects.get(username = username)
    # if student.isTutor:
    #     tutor = Tutor.objects.get(username=username)
    #     tutor.balance = float(tutor.balance) + float(amount)
    #     tutor.save()
    # else:
    #     student.balance= float(student.balance) + float(amount)
    #     student.save()
    wallet = Wallet.objects.get(username=username)
    wallet.balance = float(wallet.balance) + float(amount)
    wallet.save()
    admin = MyTutorsWallet.objects.get(username = "mytutors")
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
def mytutors_withdraw(request):
    wallet = MyTutorsWallet.objects.all()[0]
    if request.method == 'POST':
        print("here")
        to_deduct = int(request.POST["withdraw"])
        wallet = MyTutorsWallet.objects.all()[0]
        wallet.amount = wallet.amount - to_deduct;
        wallet.save();
    return render(request, 'tutoria/mytutors.html',{'wallet':wallet})

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
    return render(request, 'tutoria/index.html')

def coupon(request, code):
    print(code)
    try:
        coupon = Coupon.objects.get(code=code)
        return JsonResponse({"success" : True, "discount" : coupon.discount})
    except:
        return JsonResponse({"success" : False})

@login_required()
def dashboard(request):
    if request.user.username ==  "administrator":
        return render(request, 'tutoria/admin.html')

    if request.user.username ==  "mytutors":
        wallet = MyTutorsWallet.objects.get(username="mytutors")
        return render(request, 'tutoria/mytutors.html',{'wallet':wallet})

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

@login_required()
def manage_student_time_table(request):
    username = request.user.username
    all_sessions = get_student_sessions(username)
    all_sessions = filter_sessions(all_sessions, 7)
    week = create_week(7, 30)
    result = manage_sessions(all_sessions, week)
    return render(request, 'tutoria/mstt.html', {'sessions' : result})

@login_required()
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

@login_required(redirect_field_name='/tutoria/dashboard')
def set_profile(request):
    if request.method == 'POST':
        temp = request.POST.getlist('checks')
        isTutor = False
        isStudent = False
        if 'student' in temp:
            isStudent = True
        if 'tutor' in temp:
            isTutor = True
        # Create wallet object
        wallet = Wallet(
        username = request.user.username,
        balance = request.POST['balance'],
        )
        wallet.save()
        if temp[0] == 'tutor':
            tutor = Tutor(
                first_name = request.user.first_name,
                last_name = request.user.last_name,
                username = request.user.username,
                biography = request.POST['biography'],
                university = request.POST['university'],
                tutortype = temp[1],
                isStudent = isStudent,
                rate = request.POST['rate'],
                tags = request.POST['tags'],
                phoneNumber = request.POST['tel'],
            )
            tutor.save()
        if 'student' in temp:
            student = Student(
                name = request.user.first_name + request.user.last_name,
                username = request.user.username,
                isTutor = isTutor
            )
            student.save()
        return redirect('/tutoria/dashboard')
    return render(request, 'tutoria/setProfile.html')

@login_required()
def search(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutoria/search.html', {'tutors': tutors})

@login_required()
def nameSearch(request):
    if request.method =='GET':
        tutors = Tutor.objects.all()
        return render(request, 'tutoria/search.html', {'tutors': tutors})
    else:
        field_name = request.POST['nameSearch']
        if field_name:
            tutors = Tutor.objects.filter(Q(first_name__startswith=field_name) | Q(last_name__startswith=field_name))
            return render(request, 'tutoria/search.html', {'tutors': tutors, 'nameSearch':1})


        '''try:'''
        field_uni = request.POST['uniSearch']
        field_course = request.POST['courseSearch']
        field_sub = request.POST['subSearch']
        field_rateFrom = request.POST['rateFrom']
        field_rateTo = request.POST['rateTo']
        field_type = request.POST['typeSearch']
        field_day = request.POST['daySearch']

        #print(field_uni,field_course,field_sub,field_type)
        try:
            tutors = Tutor.objects.filter(university__startswith=field_uni,
                                          tutortype__startswith=field_type,
                                          course__startswith=field_course,
                                          subject__startswith=field_sub,
                                          rate__lt=field_rateTo,
                                          rate__gt=field_rateFrom)
        except:
            tutors = Tutor.objects.filter(university__startswith=field_uni,
                                          tutortype__startswith=field_type,
                                          course__startswith=field_course,
                                          subject__startswith=field_sub)

        if field_day =="Seven":
            t_remove=[]
            for t in tutors:
                num=len(Session.objects.filter(tutor=t))
                if t.tutortype == "private" and num == 56:
                    t_remove.append(t)
                elif t.tutortype == "contracted" and num == 112:
                    t_remove.append(t)

            tutors=tutors.exclude(id__in=[o.id for o in t_remove])

        return render(request, 'tutoria/search.html', {'tutors': tutors, 'nameSearch':1})

        '''except Exception as e:
            print(e)
            tutors = Tutor.objects.all()
            return render(request, 'tutoria/search.html', {'tutors': tutors})'''

@login_required(redirect_field_name='/tutoria/dashboard')
def view_tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    reviews=Review.objects.filter(tutor=tutor)
    return render(request, 'tutoria/viewProfile.html', {'tutor':tutor, 'reviews':reviews[::-1]})
    reviews=Review.objects.filter(tutor=tutor)
    hasRating=False
    if len(reviews)>3:
        hasRating=True
    return render(request, 'tutoria/viewProfile.html', {'tutor':tutor, 'reviews':reviews[::-1], 'hasRating':hasRating})

@login_required(redirect_field_name='/tutoria/dashboard')
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

@login_required(redirect_field_name='/tutoria/dashboard')
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
    for item in student_sessions:
        if item.tutor == tutor:
            comp = item.start_time
            if comp.day == date_time.day and comp.month == date_time.month and comp.year == date_time.year:
             return False

    return True

@login_required(redirect_field_name='/tutoria/dashboard')
def book(request, tutor_id, date_time):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    start_time = parser.parse(date_time)
    if request.method == 'POST':
        due = float(request.POST['final'])
        student = get_object_or_404(Student, username=request.user.username)
        if check_conflict(tutor, student, start_time):
            duration = 60 if tutor.tutortype == 'private' else 30
            td = datetime.timedelta(minutes=60) if tutor.tutortype == 'private' else datetime.timedelta(minutes=30)
            #  Deduct from wallet

            costOfBooking = (due + due*0.05) if tutor.tutortype == 'private' else 0
            if costOfBooking > get_balance(student.username) :
                return render(request, 'tutoria/add_funds.html', {'error' : 'Insufficient Funds !!.'})
            else:
                session = Session(
                    tutor = tutor,
                    student = student,
                    start_time = start_time,
                    end_time = start_time + td,
                    duration = duration,
                    amount = due,
                    status = 'BOOKED'
                )
                session.save()
                # Calculate commission
                commission= float(tutor.rate)*0.05
                # create transaction object
                transaction = Transaction(
                    tutor = tutor,
                    student = student,
                    start_time = start_time,
                    end_time = start_time + td,
                    amount = due,
                    commission = commission
                )
                transaction.save()

                """ Notification object """
                title="{} booked a session with {} on {}.".format(session.student,session.tutor,session.start_time)
                today=datetime.datetime.today()
                str_date="{}/{}/{}".format(today.day,today.month,today.year)
                str_time="{}:{}".format(today.hour,today.minute)
                now=int(ttime.time())
                notif=Notification(
<<<<<<< HEAD
                    title=title,
                    tutor=session.tutor,
                    student=session.student,
                    now=now,
                    date=str_date,
                    time=str_time,
                    start_time = start_time,
                    end_time = start_time + td,
                    forSession = True,
=======
                title=title,
                tutor=session.tutor,
                student=session.student,
                now=now,
                date=str_date,
                time=str_time,
                start_time = start_time,
                end_time = start_time + td,
                forSession = True,
                session=session
>>>>>>> origin/2111

                )
                print(notif.title)
                notif.save()
                """ Notification object """
                sendFundsToAdmin(student.username, costOfBooking)
                return redirect('/tutoria/dashboard')
        else:
            return render(request, 'tutoria/bookSession.html', {'error' : 'conflict with another booked slot.'})
    else:
        context = {
            'date': date_time,
            'tutor': tutor,
            'coupon' : ["1", "2"]
        }
        return render(request, 'tutoria/bookSession.html', context)

@login_required(redirect_field_name='/tutoria/dashboard')
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
            today=datetime.datetime.today()
            notif=Notification(
                title="{} cancelled session with {} scheduled for {}".format(student.username,session.tutor.username,session.start_time),
                forSession=False,
                student=student,
                tutor=session.tutor,
                now=int(ttime.time()),
                date="{}/{}/{}".format(today.day,today.month,today.year),
                time="{}:{}".format(today.hour,today.minute)

                )
            print(notif.title)
            notif.save()
            return redirect('/tutoria/dashboard')
    else:
        context = {
            'session_id':session.id,
            'tutor' : session.tutor,
            'tutor_no':session.tutor.phoneNumber,
            'start' : session.start_time,
            'end' : session.end_time,
            'duration': session.duration
        }
        return render(request, 'tutoria/session_detail.html', context)

@login_required()
def add_funds(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        # student = Student.objects.get(username = request.user.username)
        # if student.isTutor:
        #     tutor = Tutor.objects.get(username=request.user.username)
        #     tutor.balance = float(tutor.balance) + float(amount)
        #     tutor.save()
        # else:
        #     student.balance= float(student.balance) + float(amount)
        #     student.save()
        wallet = Wallet.objects.get(username=request.user.username)
        wallet.balance = float(wallet.balance)+float(amount)
        wallet.save()
        return redirect('/tutoria/dashboard')
    else:
        return render(request, 'tutoria/add_funds.html')

# Withdraw funds for tutor
@login_required()
def withdraw_funds(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        # student = Student.objects.get(username = request.user.username)
        # if student.isTutor:
        #     tutor = Tutor.objects.get(username=request.user.username)
        #     tutor.balance = float(tutor.balance) + float(amount)
        #     tutor.save()
        # else:
        #     student.balance= float(student.balance) + float(amount)
        #     student.save()
        wallet = Wallet.objects.get(username=request.user.username)
        if float(amount) > float(wallet.balance) :
            return render(request, 'tutoria/withdraw_funds.html', {error : "Insufficient funds !!!"})
        else :
            wallet.balance = float(wallet.balance)-float(amount)
            wallet.save()
        return redirect('/tutoria/dashboard')
    else:
        return render(request, 'tutoria/withdraw_funds.html')

@login_required()
def notifications(request):
    if request.method=="GET":
        s1=Student.objects.filter(username=request.user.username)
        if len(s1)>=0:
            s=s1
        else:
            s=None
        tutor=None
        student=None
        if s:
            student=s
        else:
            tutor=Tutor.objects.filter(username=request.user.username)
        stu_notifs=Notification.objects.filter(student=student)
        tut_notifs=Notification.objects.filter(tutor=tutor)
        # stu_notifs=Notification.objects.filter(student=user)
        notifs=[]
        for x in tut_notifs:
            notifs.append(x)
        for y in stu_notifs:
            notifs.append(y)

        notifs.sort(key=lambda x: x.now, reverse=True)

        return render(request,'tutoria/notifications.html/',{'notifs':notifs})

@login_required(redirect_field_name='/tutoria/dashboard')
def review(request,session_id):
    if request.method=="POST":
        session=get_object_or_404(Session,pk=session_id)
        rev=Review(
            student=session.student,
            tutor=session.tutor,
            text=request.POST['review'],
            rating=request.POST['rating']
            )
        rev.save()
        tut=session.tutor
        revs=Review.objects.filter(tutor=tut)

        if len(revs)>3:
            tot=0
            for rev in revs:
                tot=tot+rev.rating
            avg=tot/len(revs)
            tut.rating=avg
            tut.hasRating=True
            tut.save()
        return redirect('/tutoria/dashboard')

    else:
        return render(request, 'tutoria/writeReview.html')




@login_required()
def edit_profile(request):
    if request.method == 'POST':
        tutor = Tutor.objects.get(username=request.user.username)
        tutor.first_name = request.POST['first_name']
        tutor.last_name = request.POST['last_name']
        tutor.biography = request.POST['biography']
        tutor.university = request.POST['university']
        tutor.rate = request.POST['rate']
        isHidden = request.POST.get('isHidden', False)
        tutor.isHidden = isHidden
        tutor.phoneNumber = request.POST['tel']
        tutor.tags = request.POST['tags']
        if len(request.FILES) != 0:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            avatar = fs.save(str(myfile),myfile)
            tutor.avatar = avatar
        tutor.save()
        return redirect('/tutoria/dashboard')
    else:
        tutor = Tutor.objects.get(username=request.user.username)
        return render(request, 'tutoria/editProfile.html',{"tutor" : tutor})
