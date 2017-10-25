from django.contrib import admin
from .models import Tutor, Student, Transaction, Session
# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Transaction)
admin.site.register(Session)
