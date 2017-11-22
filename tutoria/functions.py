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
