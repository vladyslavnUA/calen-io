from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'cal'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url(r'^event/(?P<event_id>\d+)/$', views.detail, name='event_detail'),
]