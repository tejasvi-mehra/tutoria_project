from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import MyTutorsWallet, Course, Tutor, Student, Transaction, Wallet, Session
from django.contrib.admin import AdminSite


admin.site.register(MyTutorsWallet)
admin.site.register(Course)
# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Transaction)
admin.site.register(Session)
admin.site.register(Wallet)
