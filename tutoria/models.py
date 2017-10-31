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
    discount = models.DecimalField(decimal_places=0, max_digits=3, default=0)

    def __str__(self):
        return self.amount

class Session(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date = models.CharField(max_length=100, default="")
    time = models.CharField(max_length=100, default="")
    # startTime = models.DateTimeField(null=True, blank=True)
    # endTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.tutor.username
