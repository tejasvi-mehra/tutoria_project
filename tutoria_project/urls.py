from django.conf.urls import url, include
from django.contrib import admin
# from tutoria.models import AdminWallet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', include('tutoria.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tutoria/', include('tutoria.urls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^f1d18551.ngrok.io/', include('tutoria.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
