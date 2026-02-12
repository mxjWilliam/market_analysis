"""
URL configuration for market_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import  views
from django.urls import path

app_name = 'short_emotion'

urlpatterns = [
    path('add', views.add_short_emotion_data, name='add_short_emotion_data'),
    path('query_all', views.query_all, name='query_all'),
    path('total_floor', views.total_floor_data, name='total_floor_data'),
    path('up_down', views.up_down_data, name='up_down_data'),
    path('up_down_floor', views.up_down_floor_data, name='up_down_floor_data'),
    path('admin_updown', views.admin_updown_number, name='admin_updown_number'),
]
