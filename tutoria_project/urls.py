from django.conf.urls import url, include
from django.contrib import admin
from tutoria.models import AdminWallet

TutoriaAdmin= AdminWallet.objects.get(username = "admin")
admin.site.index_title = "Amount: " + str(TutoriaAdmin.amount)
# print (TutoriaAdmin.balance)
urlpatterns = [
    url(r'^$', include('tutoria.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tutoria/', include('tutoria.urls')),
]
