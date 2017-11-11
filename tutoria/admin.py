from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

# from django.db import models
from .models import Tutor, Student, Transaction, Session, AdminWallet
# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Transaction)
admin.site.register(Session)
admin.site.register(AdminWallet)
