from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('admin_calendar', views.admin_calendar, name='admin_calendar'),
]
