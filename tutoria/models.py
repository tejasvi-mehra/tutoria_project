from django.db import models
import json

class Tutor(models.Model):
    name = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=100)
    biography = models.CharField(max_length=10000)
    university = models.CharField(max_length=100)
    tutortype = models.CharField(max_length=10)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    isStudent = models.BooleanField(default=False)
    rate = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=100)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    isTutor = models.BooleanField(default=False)

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
