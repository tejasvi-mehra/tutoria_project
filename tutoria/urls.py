from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', auth_views.login ,  name='login'),

    url(r'^logout/$', auth_views.logout ,  {'next_page' : 'home'}, name='logout'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^setProfile/$', views.set_profile, name='dashboard'),

    url(r'^search/$', views.search, name='search'),

    url(r'^nameSearch/$', views.nameSearch, name='nameSearch'),

    url(r'^book/(?P<tutor_id>[0-9]+)/(?P<date_time>.*)/$', views.book, name='book'),

    url(r'^cancel/(?P<date_time>.*)/$', views.detail_cancel, name='cancel'),

    url(r'^view_profile/(?P<tutor_id>[0-9]+)/$', views.view_tutor_profile, name='view_profile'),

    url(r'^viewTimetable/(?P<tutor_id>[0-9]+)/$', views.view_tutor_timetable, name='view_timetable'),

    url(r'^manage_timetable/student/$', views.manage_student_time_table, name='manage_student_time_table'),

    url(r'^manage_timetable/tutor/$', views.manage_tutor_time_table, name='manage_student_time_table'),

    url(r'^session_detail/(?P<date_time>.*)/$', views.detail_cancel, name='session_detail'),

    url(r'^session_tutor/(?P<date_time>.*)/$', views.session_tutor, name='session_detail'),

    url(r'^tutor_block_session/(?P<date_time>.*)/$', views.tutor_block_session, name='tutor_block_session'),

    url(r'^tutor_unblock_session/(?P<date_time>.*)/$', views.tutor_unblock_session, name='tutor_unblock_session'),

    url(r'^add_funds/$', views.add_funds, name='add_funds'),

    url(r'^withdraw_funds/$', views.withdraw_funds, name='withdraw_funds'),

    url(r'^notifications/',views.notifications,name='notifications'),

    url(r'^writeReview/(?P<session_id>.*)/$',views.review,name='review'),

    url(r'^edit_profile/(?P<tutor_id>[0-9]+)/$', views.edit_profile, name='edit_profile'),

    url(r'^coupon/(?P<code>.*)/$',views.coupon, name='coupon'),

    url(r'^mytutors/withdraw/$', views.mytutors_withdraw , name='mytutors_withdraw'),

    url(r'^admin_panel/$', views.admin_panel , name='mytutors_withdraw'),
]
