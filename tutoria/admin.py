# from django.contrib import admin
# from django.contrib.admin import AdminSite
# from django.utils.translation import ugettext_lazy
#
# # from django.db import models
# from .models import Tutor, Student, Transaction, Session, AdminWallet
# # Register your models here.
# admin.site.register(Tutor)
# admin.site.register(Student)
# admin.site.register(Transaction)
# admin.site.register(Session)
# admin.site.register(AdminWallet)



####################


from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import AdminWallet, Course, Tutor, Student, Transaction, Wallet, Session
from django.contrib.admin import AdminSite
#Tutor, Student, Transaction, Session,





#
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ["code","subject"]
#     class Meta:
#         model = Course
#
#     def has_change_permission(self, request, obj=None):
#         return True
#     def has_delete_permission(self, request, obj=None):
#         return False
#     def has_add_permission(self, request):
#         return True

#
# class MyAdminSite(AdminSite):
#     site_header = 'Monty Python administration'
#     usern=AdminWallet.objects.get(username="admin")
#     index_title = str(usern.amount)
    # index_template = "/home/krohak/Documents/SE/tutoria_project/tutoria_project/templates/admin/view.html"

#
# admin.site = MyAdminSite(name='myadmin')
#
#

admin.site.register(AdminWallet)
admin.site.register(Course)
# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Transaction)
admin.site.register(Session)
admin.site.register(Wallet)

'''
class PostAdmin(admin.ModelAdmin):
    list_display = ["amount"]
    class Meta:
        model = AdminWallet

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        del actions["delete_selected"]
        return actions

    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
'''

'''    def __init__(self, *args, **kwargs):
        super(PostAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
'''



'''    def __init__(self, *args, **kwargs):
         super(PostAdmin, self).__init__(*args, **kwargs)
         self.readonly_fields = self.model._meta.get_all_field_names()
'''
'''
class GroupAdmin(admin.ModelAdmin):
    class Meta:
        model = Group

    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return True
'''
