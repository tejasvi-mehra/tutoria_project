from django.conf.urls import url, include
from django.contrib import admin
from tutoria.models import AdminWallet
from django.conf import settings
from django.conf.urls.static import static

# TutoriaAdmin= AdminWallet.objects.get(username = "admin")
# admin.site.index_title = "Amount: " + str(TutoriaAdmin.amount)
# print (TutoriaAdmin.balance)
urlpatterns = [
    url(r'^$', include('tutoria.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tutoria/', include('tutoria.urls')),
    url('^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
