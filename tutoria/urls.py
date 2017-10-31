from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', auth_views.login ,  name='login'),

    url(r'^logout/$', auth_views.logout ,  name='login'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^setProfile/$', views.setProfile, name='dashboard'),

    url(r'^search/$', views.search, name='search'),

    url(r'^nameSearch/$', views.nameSearch, name='nameSearch'),

    url(r'^book/(?P<tutor_id>[0-9]+)/(?P<date>.*)/(?P<time>.*)/$', views.book, name='book'),

    url(r'^cancel/(?P<date>.*)/(?P<time>.*)/$', views.cancel, name='cancel'),

    url(r'^viewProfile/(?P<tutor_id>[0-9]+)/$', views.viewProfile, name='viewProfile'),

    url(r'^viewTimetable/(?P<tutor_id>[0-9]+)/$', views.viewTimetable, name='viewTimetable'),


]
