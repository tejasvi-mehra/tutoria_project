from django.db import models
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
import time
# from dateutil.parser import *
from datetime import date, datetime


class Tutor(models.Model):
    last_name = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=100)
    biography = models.CharField(max_length=10000)
    university = models.CharField(max_length=100)
    tutortype = models.CharField(max_length=10)
    isStudent = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)
    course = models.CharField(max_length=10, default="")
    subject = models.CharField(max_length=100, default="")
    phoneNumber = models.IntegerField(default=99999999)
    avatar = models.FileField(default="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
    isHidden =  models.BooleanField(default=False)
    tags = models.CharField(max_length=10000, default="")

    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=100)
    isTutor = models.BooleanField(default=False)
    phoneNumber = models.DecimalField(decimal_places=0, max_digits=10, default=99999999)

    def __str__(self):
        return self.username

class Transaction(models.Model):
    student = models.ForeignKey(Student)
    tutor = models.ForeignKey(Tutor)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    commission = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    discount = models.DecimalField(decimal_places=0, max_digits=3, default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student) + " to " + str(self.tutor) + " at " + str(self.start_time) + " val " + str(self.completed)

class Session(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True,on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=100, default="") # BOOKED || BLOCKED
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField()

    def __str__(self):
        if self.student:
            return "booked by " + self.student.username + " with "  + self.tutor.username
        else:
            return "blocked by " + self.tutor.username

class AdminWallet(models.Model):
    username = models.CharField(max_length=100, default="admin")
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    def __self__ (self):
        return "Amount: " + self.amount

class Notification(models.Model):

    title = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    forSession=models.BooleanField(default=True)
    viewed_stu = models.BooleanField(default=False)
    viewed_tut = models.BooleanField(default=False)
    now=models.DecimalField(decimal_places=2, max_digits=13, default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    date=models.CharField(max_length=200)
    time=models.CharField(max_length=200)

class Review(models.Model):
    """docstring for Review"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    rating = models.IntegerField()


@receiver(post_save, sender=User)
def send_notif(sender, **kwargs):
    print("New Notification")

class Course(models.Model):
    code = models.CharField(max_length=10, default="")
    subject = models.CharField(max_length=100, default="")

class Wallet(models.Model):
    username = models.CharField(max_length=100)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    def __str__(self):
        return "Balance for " + self.username + " :" + str(self.balance)
