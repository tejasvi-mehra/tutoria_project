from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Tutor, Student, Session, Transaction, MyTutorsWallet, Notification, Review, Wallet, Coupon, Course
from django.db.models import Q
import datetime
from dateutil import parser
from datetime import date
import time as ttime
from django.core.files.storage import FileSystemStorage, Storage
from django.http import JsonResponse
from .functions import *

def mytutors_withdraw(request):
    wallet = MyTutorsWallet.objects.all()[0]
    if request.method == 'POST':
        print("here")
        to_deduct = int(request.POST["withdraw"])
        wallet = MyTutorsWallet.objects.all()[0]
        wallet.balance = wallet.balance - to_deduct;
        wallet.save();
    return render(request, 'tutoria/funds/mytutors.html',{'wallet':wallet})

def home(request):
    return render(request, 'tutoria/index.html')

def coupon(request, code):
    print(code)
    try:
        coupon = Coupon.objects.get(code=code)
        return JsonResponse({"success" : True, "discount" : coupon.discount})
    except:
        return JsonResponse({"success" : False})

def admin_panel(request):
    if request.method == 'POST':
        if request.POST['remsub']:
            Course.objects.all().delete()
            remsub = request.POST['remsub']
            courselist = str(remsub).split(',')
            xs = [str(x).split(':') for x in courselist]
            for id_i,code in enumerate(xs):
                course = Course(subject=xs[id_i][1],code=xs[id_i][0])
                course.save()
        else:
            Course.objects.all().delete()

        if request.POST['sub']:
            sub=request.POST['sub']
            code=request.POST['code']
            course = Course(
            subject = sub,
            code = code,
            )
            course.save()

    return render(request, 'tutoria/admin.html',{'courses':Course.objects.all()})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/tutoria/set_profile/')
    else:
        form = RegisterForm()
    return render(request, 'tutoria/profile/register.html', {'form' : form})

@login_required()
def dashboard(request):
    if request.user.username ==  "administrator":
        return render(request, 'tutoria/admin.html',{'courses':Course.objects.all()})

    if request.user.username ==  "mytutors":
        wallet = MyTutorsWallet.objects.get(username="mytutors")
        return render(request, 'tutoria/funds/mytutors.html',{'wallet':wallet})

    username = request.user.username
    tutor_sessions, student_sessions = get_sessions(username)
    tutor_sessions.sort(key=lambda x:x.start_time)
    student_sessions.sort(key=lambda x:x.start_time)

    student, tutor = check_person(username)
    if tutor == False:
        name = student.name
    else :
        name = tutor.first_name + " " + tutor.last_name
    balance = get_balance(username)
    print ('coming here')
    transactions_outgoing = get_transactions_outgoing(username)
    transactions_incoming = get_transactions_incoming(username)
    context = {
        'name' : name,
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
    return render(request, 'tutoria/timetable/mstt.html', {'sessions' : result})

@login_required()
def session_tutor(request, date_time):
    toview = parser.parse(date_time)
    tutor = Tutor.objects.get(username = request.user.username)
    session = Session.objects.get(tutor = tutor, start_time=toview)
    return render(request, 'tutoria/session/session_tutor.html', {'session' : session})

@login_required()
def manage_tutor_time_table(request):
    error = ""
    if request.GET.get('error'):
        error = request.GET['error']
    username = request.user.username
    all_sessions = get_tutor_sessions(username)
    all_sessions = filter_sessions(all_sessions, 14)
    tutor = Tutor.objects.get(username=username)
    week = create_week(14, 60) if tutor.tutortype == 'private' else create_week(14, 30)
    result = manage_sessions(all_sessions, week)
    context = {
        'sessions' : result,
        'error' : error
    }
    if tutor.tutortype == 'private':
        print("here whats up")
        return render(request, 'tutoria/timetable/mtttp.html', context)
    else:
        print("here whats up")
        return render(request, 'tutoria/timetable/mtttc.html', context)

@login_required(redirect_field_name='/tutoria/dashboard')
def set_profile(request):
    if request.method == 'POST':
        temp = request.POST.getlist('checks')
        isTutor = True if 'tutor' in temp else False
        isStudent = True if 'student' in temp else False

        avatar = ""

        if temp[0] == 'tutor':
            course_tut=""
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

            if len(request.FILES) != 0:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                avatar = fs.save(str(myfile),myfile)
                tutor.avatar = avatar

            try:
                course_tut = Course.objects.get(subject__iexact=request.POST['sub'],code=request.POST['code'])
                tutor.course.add(course_tut)
            except:
                pass

            tutor.save()

        if 'student' in temp:
            student = Student(
                name = request.user.first_name + " " + request.user.last_name,
                username = request.user.username,
                isTutor = isTutor,
            )
            if len(request.FILES) != 0:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                avatar = fs.save(str(myfile),myfile)
                student.avatar = avatar
            student.save()

        wallet = Wallet(
            username = request.user.username,
            balance = request.POST['balance'],
        )
        wallet.save()
        return redirect('/tutoria/dashboard')
    return render(request, 'tutoria/profile/set_profile.html')

@login_required()
def search(request):
    tutors = Tutor.objects.filter(isHidden=False)
    username = request.user.username
    student, tutor = check_person(username)
    return render(request, 'tutoria/search.html', {'tutors': tutors,'student':student,'tutor':tutor})

@login_required()
def nameSearch(request):
    username = request.user.username
    student, tutor = check_person(username)
    if request.method =='GET':
        tutors = Tutor.objects.filter(isHidden=False)
        return render(request, 'tutoria/search.html', {'tutors': tutors,'student':student,'tutor':tutor})
    else:
        field_name = request.POST['nameSearch']
        if field_name:
            try:
                name=str(field_name).split(' ') #both first_name and last_name
                tutors = Tutor.objects.filter(Q(first_name__startswith=name[0],last_name__startswith=name[1]),isHidden=False)
                return render(request, 'tutoria/search.html', {'tutors': tutors,'student':student,'tutor':tutor})
            except:
                tutors = Tutor.objects.filter(Q(first_name__startswith=field_name) | Q(last_name__startswith=field_name),isHidden=False)
                return render(request, 'tutoria/search.html', {'tutors': tutors,'student':student,'tutor':tutor})


        field_uni = request.POST['uniSearch']
        field_course = request.POST['courseSearch']
        field_sub = request.POST['subSearch']
        field_rateFrom = request.POST['rateFrom']
        field_rateTo = request.POST['rateTo']
        field_type = request.POST['typeSearch']
        field_day = request.POST['daySearch']
        field_tags = request.POST['tags']

        kk = Course.objects.filter(code__startswith=field_course,subject__istartswith=field_sub)
        tutors=""
        if (field_rateTo or field_rateFrom):
            tutors = Tutor.objects.filter(university__istartswith=field_uni,
                                          tutortype__startswith=field_type,
                                          course__in=kk,
                                          rate__lte=field_rateTo,
                                          rate__gte=field_rateFrom,
                                          tags__icontains=field_tags,
                                          isHidden=False).distinct()


        else:
            tutors = Tutor.objects.filter(university__istartswith=field_uni,
                                          tutortype__startswith=field_type,
                                          course__in=kk,
                                          tags__icontains=field_tags,
                                          isHidden=False).distinct()
            print([k for k in tutors])
        if field_day =="Seven":
            t_remove=[]
            for t in tutors:
                num=len(Session.objects.filter(tutor=t))
                l=Session.objects.filter(tutor=t)
                print(num, [g.start_time for g in l])
                if t.tutortype == "private" and num >= 56:
                    t_remove.append(t)
                elif t.tutortype == "contracted" and num >= 96:
                    t_remove.append(t)

            tutors=tutors.exclude(id__in=[o.id for o in t_remove])

        return render(request, 'tutoria/search.html', {'tutors': tutors,'student':student,'tutor':tutor})

@login_required(redirect_field_name='/tutoria/dashboard')
def view_tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    tags = tutor.tags.split(',');
    reviews=Review.objects.filter(tutor=tutor)
    hasRating=False
    available = True
    if len(reviews)>=3:
        hasRating=True
    num=len(Session.objects.filter(tutor=tutor))
    if tutor.tutortype == "private" and num == 56:
        available = False
    elif tutor.tutortype == "contracted" and num == 112:
        available = False
    context = {
        'tutor':tutor,
        'reviews':reviews[::-1],
        'hasRating':hasRating,
        'tags' :tags[:6],
        'isAvailable': available
    }
    if request.user.username == tutor.username:
        return render(request, 'tutoria/profile/t_view_profile.html', context)
    else:
        return render(request, 'tutoria/profile/s_view_profile.html', context)

@login_required(redirect_field_name='/tutoria/dashboard')
def tutor_block_session(request, date_time):
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
        return redirect('/tutoria/manage_timetable/tutor')
    else:
        return redirect('/tutoria/manage_timetable/tutor?error=This session has already been booked')

@login_required(redirect_field_name='/tutoria/dashboard')
def tutor_unblock_session(request, date_time):
    tounlock = parser.parse(date_time)
    tutor = Tutor.objects.get(username=request.user.username)
    session = Session.objects.get(tutor=tutor, start_time=tounlock)
    session.delete();
    return redirect('/tutoria/manage_timetable/tutor')

@login_required(redirect_field_name='/tutoria/dashboard')
def view_tutor_timetable(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    sessions = filter_sessions(get_tutor_sessions(tutor.username), 7)
    week = create_week(7, 60) if tutor.tutortype == 'private' else create_week(7, 30)
    result = manage_sessions(sessions, week)
    context = {
        'tutor' : tutor,
        'sessions' : result
    }
    if tutor.tutortype == 'private':
        return render(request, 'tutoria/timetable/vttp.html', context)
    else:
        return render(request, 'tutoria/timetable/vttc.html', context)

@login_required(redirect_field_name='/tutoria/dashboard')
def book(request, tutor_id, date_time):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    start_time = parser.parse(date_time)
    tdy = datetime.datetime.today()
    if request.method == 'POST':
        due = float(request.POST['final'])
        commission = float(tutor.rate)*0.05
        student = get_object_or_404(Student, username=request.user.username)
        costOfBooking = (due) if tutor.tutortype == 'private' else 0
        if costOfBooking + commission > get_balance(student.username) :
            context = {
                'error' : 'Insufficient Funds !!.',
                'date': date_time,
                'tutor': tutor,
                'balance' : get_balance(student.username)
            }
            return render(request, 'tutoria/funds/add_funds.html', context)
        flag, error = check_conflict(tutor, student, start_time)
        if flag:
            duration = 60 if tutor.tutortype == 'private' else 30
            td = datetime.timedelta(minutes=60) if tutor.tutortype == 'private' else datetime.timedelta(minutes=30)

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

            transaction = Transaction(
                tutor = tutor,
                student = student,
                session_start_time = start_time,
                session_end_time = start_time + td,
                booked_time = tdy,
                session = session,
                amount = due,
                commission = commission
            )
            transaction.save()


            title="{} booked a session with you on {}.".format(session.student,session.start_time)
            today=datetime.datetime.today()
            str_date="{}/{}/{}".format(today.day,today.month,today.year)
            str_time="{}:{}".format(today.hour,today.minute)
            created_at=int(ttime.time())
            notif=Notification(

                title=title,
                tutor=session.tutor,
                student=None,
                created_at = created_at,
                date=str_date,
                time=str_time,
                forSession = True,
                session=session

            )
            print("To: {}".format(session.tutor.username)+"\nFrom: MyTutors\nSubject: Session Activity")
            print("Dear {},\n".format(session.tutor.first_name+" "+session.tutor.last_name))
            print(notif.title)
            # notif2.save()
            notif.save()
            title2="You booked a session with {} on {}.".format(session.tutor,session.start_time)
            notif2=Notification(

                title=title2,
                tutor=None,
                student=session.student,
                created_at = created_at,
                date=str_date,
                time=str_time,
                forSession = True,
                session=session

            )
            # print(notif2.title)
            notif2.save()

            sendFundsToMyTutors(student.username, costOfBooking+commission)
            return redirect('/tutoria/session_detail/' + str(session.start_time))
        else:
            context = {
                'error' : error,
                'date': date_time,
                'tutor': tutor
            }
            return render(request, 'tutoria/session/bookSession.html', context)
    else:
        context = {
            'date': date_time,
            'tutor': tutor,
        }
        return render(request, 'tutoria/session/bookSession.html', context)

@login_required(redirect_field_name='/tutoria/dashboard')
def session_detail(request, date_time):
    tocancel = parser.parse(date_time)
    student = Student.objects.get(username = request.user.username)
    session = Session.objects.get(student = student, start_time=tocancel)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    canCancel = True
    if session.start_time < tdy:
        canCancel = False
    print(canCancel)
    error = ''
    if request.method == 'POST':
        if session.start_time > tdy + datetime.timedelta(hours=24):
            transaction = Transaction.objects.get(student = student, session_start_time = tocancel)
            refund_amount = transaction.amount + transaction.commission
            refundFromMyTutors(student.username, refund_amount)
            session.delete()
            transaction1 = Transaction(
                booked_time = tdy,
                session_start_time = transaction.session_start_time,
                session_end_time = transaction.session_end_time,
                session = None,
                student = transaction.student,
                tutor = transaction.tutor,
                completed = True,
                commission = transaction.commission,
                amount = transaction.amount
            )
            transaction1.save()
            # transaction.delete()
            today=datetime.datetime.today()
            notif=Notification(
                title="You cancelled session with {} scheduled for {}".format(session.tutor,session.start_time),
                forSession=False,
                student=session.student,
                tutor=None,
                created_at = int(ttime.time()),
                date="{}/{}/{}".format(today.day,today.month,today.year),
                time="{}:{}".format(today.hour,today.minute)

                )
            print(notif.title)
            notif.save()
            notif2=Notification(
                title="{} cancelled session with you scheduled for {}".format(session.student,session.start_time),
                forSession=False,
                student=None,
                tutor=session.tutor,
                created_at = int(ttime.time()),
                date="{}/{}/{}".format(today.day,today.month,today.year),
                time="{}:{}".format(today.hour,today.minute)

                )
            print("To: {}".format(session.tutor.username)+"\nFrom: MyTutors\nSubject: Session Activity")
            print("Dear {},\n".format(session.tutor.first_name+" "+session.tutor.last_name))
            print(notif2.title)
            notif2.save()
            return redirect('/tutoria/dashboard')
        else:
            error = "You can't cancel a session which starts in less than 24 hours. Sorry."

    context = {
        'session' : session,
        'error' : error,
        'canCancel' : canCancel
    }
    return render(request, 'tutoria/session/session_detail.html', context)

@login_required()
def add_funds(request):
    wallet = Wallet.objects.get(username=request.user.username)
    if request.method == 'POST':
        amount = request.POST['amount']
        wallet.balance = float(wallet.balance) + float(amount)
        wallet.save()
        return redirect('/tutoria/dashboard')
    else:
        return render(request, 'tutoria/funds/add_funds.html', {'balance' : wallet.balance})

@login_required()
def withdraw_funds(request):
    wallet = Wallet.objects.get(username=request.user.username)
    if request.method == 'POST':
        amount = request.POST['amount']
        if float(amount) > float(wallet.balance) :
            return render(request, 'tutoria/funds/withdraw_funds.html', {"error" : "Insufficient funds !!!", 'balance' : wallet.balance})
        else :
            wallet.balance = float(wallet.balance)-float(amount)
            wallet.save()
        return redirect('/tutoria/dashboard')
    else:
        return render(request, 'tutoria/funds/withdraw_funds.html', {'balance' : wallet.balance})

@login_required()
def notifications(request):
    if request.method=="GET":

        student = None
        tutor = None

        student1 = Student.objects.filter(username=request.user.username)
        tutor1 = Tutor.objects.filter(username=request.user.username)

        if len(student1) > 0:
            student = student1[0]
        if len(tutor1) > 0:
            tutor = tutor1[0]

        notifications = []

        if student:
            student_notifications = Notification.objects.filter(student=student)
            for item in student_notifications:
                notifications.append(item)
        if tutor:
            tutor_notifications = Notification.objects.filter(tutor=tutor)
            for item in tutor_notifications:
                notifications.append(item)

        notifications.sort(key=lambda x: x.created_at, reverse=True)
        context = {
            'notifs' : notifications,
            'tutor' : tutor,
            'student' : student
        }
        return render(request,'tutoria/notifications.html/', context)

@login_required(redirect_field_name='/tutoria/dashboard')
def review(request,session_id):
    if request.method=="POST":
        session=get_object_or_404(Session,pk=session_id)
        rev = Review(
            student=session.student,
            tutor=session.tutor,
            text=request.POST['review'],
            rating=request.POST['rating']
            )
        rev.save()
        tut=session.tutor
        revs=Review.objects.filter(tutor=tut)

        if len(revs)>=3:
            tot=0
            for rev in revs:
                tot=tot+rev.rating
            avg=tot/len(revs)
            tut.rating=avg
            tut.hasRating=True
            tut.save()
        return redirect('/tutoria/dashboard')

    else:
        return render(request, 'tutoria/write_review.html')

@login_required()
def edit_profile(request, tutor_id):
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
        remsub = request.POST['remsub']
        course_tut=""
        ls =[]
        tutor.course.clear()
        courselist = str(remsub).split(',')
        xs = [str(x).split(':') for x in courselist]
        for id_i,code in enumerate(xs):
            try:
                courselist = Course.objects.get(subject=xs[id_i][1],code=xs[id_i][0])
                print(courselist)
                tutor.course.add(courselist)
            except:
                print('y')

        if request.POST['sub'] or request.POST['code']:
            try:
                course_tut = Course.objects.get(subject__iexact=request.POST['sub'],code=request.POST['code'])
                tutor.course.add(course_tut)
            except:
                return render(request, 'tutoria/profile/editProfile.html', {'error': 'Invalid Course Specified', 'tutor' : tutor})

        if len(request.FILES) != 0:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            avatar = fs.save(str(myfile),myfile)
            tutor.avatar = avatar
        tutor.save()

        return redirect('/tutoria/view_profile/' + str(tutor.id))
        # return render(request, 'tutoria/profile/editProfile.html',{"tutor" : tutor})
    else:
        tutor = Tutor.objects.get(username=request.user.username)
        return render(request, 'tutoria/profile/editProfile.html',{"tutor" : tutor})

@login_required()
def add_coupon(request):
    print("here")
    if request.method == "POST":
        code = request.POST['code']
        discount = request.POST['discount']
        expire = request.POST['expire']
        coupon = Coupon(code=code, discount=discount)
        coupon.save()
        return render(request, 'tutoria/admin.html')
