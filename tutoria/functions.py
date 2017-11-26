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

# filters session based on days looking ahead.
def filter_sessions(sessions, days):
    time_delta = datetime.timedelta(days=days)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    week = tdy + time_delta
    final = []
    for sesh in sessions:
        if sesh.start_time >= tdy and sesh.start_time < week:
            final.append(sesh)
    return final

# filter the transaction array based on number of days
def filter_transactions(transactions, days):
    time_delta = datetime.timedelta(days=days)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    month = tdy - time_delta
    final = []
    print(transactions)
    print('------------')
    for transaction in transactions:
        print("key", transaction)
        if transaction.booked_time <= tdy and transaction.booked_time > month and transaction.session != None:
            print("valid", transaction)
            final.append(transaction)
            print('--------')
            print("added", final)
    print('--------')
    print ("final", final)
    print ("return back")
    return final

def filter_transactions_incoming(transactions, days):
    time_delta = datetime.timedelta(days=days)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    month = tdy - time_delta
    final = []
    print(transactions)
    print('------------')
    for transaction in transactions:
        print("key", transaction)
        if transaction.booked_time <= tdy and transaction.booked_time > month and transaction.session == None:
            print("valid", transaction)
            final.append(transaction)
            print('--------')
            print("added", final)
    print('--------')
    print ("final", final)
    print ("return back")
    return final

def filter_transactions_incoming_tutor(transactions, days):
    time_delta = datetime.timedelta(days=days)
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    month = tdy - time_delta
    final = []
    print(transactions)
    print('------------')
    for transaction in transactions:
        print("key1", transaction)
        if transaction.booked_time <= tdy and transaction.booked_time > month and transaction.session != None:
            print("valid1", transaction)
            final.append(transaction)
            print('--------')
            print("added1", final)
    print('--------')
    print ("final1", final)
    print ("return back1")
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
    booked = []
    try:
        student = Student.objects.get(username=username)
        try:
            booked = student.session_set.all()
        except:
            booked = []
    except:
        booked = []
    return booked

# look at function and understand
def get_sessions(username):
    tutor_sessions = get_tutor_sessions(username)
    student_sessions = get_student_sessions(username)
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
            if item['time'] > sesh.start_time and item['time'] < sesh.end_time:
                item['status'] = "MIDDLE"
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
    wallet = Wallet.objects.get(username=username)
    return wallet.balance;

# Transfer money from student to admin on every booking
def sendFundsToMyTutors(username, amount):
    wallet = Wallet.objects.get(username=username)
    wallet.balance = float(wallet.balance)-amount
    wallet.save()
    mytutorswallet = MyTutorsWallet.objects.get(username = "mytutors")
    mytutorswallet.balance = float(mytutorswallet.balance) + amount
    mytutorswallet.save()

# Refund money back to student
def refundFromMyTutors(username, amount):
    wallet = Wallet.objects.get(username=username)
    wallet.balance = float(wallet.balance) + float(amount)
    wallet.save()
    mytutorswallet = MyTutorsWallet.objects.get(username = "mytutors")
    mytutorswallet.balance = float(mytutorswallet.balance) - float(amount)
    mytutorswallet.save()


def get_transactions_outgoing(username):
    booked = []
    print("reached ")
    try:
        student = Student.objects.get(username=username)
        try:
            student = Student.objects.get(username=username)
            print(student)
            booked = student.transaction_set.all()
            print ("called1")
            booked = filter_transactions(booked,30)
            print ("booked:")
            print (booked)
            # print(booked[0])
        except:
            booked = []
    except:
        booked = []

    return booked

def get_transactions_incoming(username):
    booked = []
    try:
        student = Student.objects.get(username=username)
        try:
            booked = student.transaction_set.all()
            print ("called2")
            booked = filter_transactions_incoming(booked,30)
            booked1 = []
            if student.isTutor :
                tutor = Tutor.objects.get(username=username)
                booked1 = tutor.transaction_set.all()
                print ("called3")
                booked1 = filter_transactions_incoming_tutor(booked1,30)
                booked = booked + booked1

        except:
            booked = []
    except:
        tutor = Tutor.objects.get(username=username)
        try:
            booked = tutor.transaction_set.all()
            print ("called3")
            booked = filter_transactions_incoming_tutor(booked,30)
        except:
            booked = []

    return booked


# check conflict while booking a session
def check_conflict(tutor, student, date_time):
    tdy = datetime.datetime.today() + datetime.timedelta(hours=8)
    print(date_time < datetime.datetime.today() + datetime.timedelta(hours=24))
    if student.username == tutor.username:
        return False, "You cannot book a session with yourself."
    if date_time < tdy + datetime.timedelta(hours=24):
        return False, "You cannot book a timeslot which start within 24 hours."
    tutor_sessions = filter_sessions(get_tutor_sessions(tutor.username), 7)
    student_sessions  = filter_sessions(get_student_sessions(student.username), 7)
    sessions = tutor_sessions + student_sessions
    for item in sessions:
        if item.start_time <= date_time and date_time < item.end_time:
            return False, "You have a conflict with another session."
    for item in student_sessions:
        if item.tutor == tutor:
            comp = item.start_time
            if comp.day == date_time.day and comp.month == date_time.month and comp.year == date_time.year:
             return False, "You can only book one session per tutor per day."

    return True, ""

""" functions to be imported """
