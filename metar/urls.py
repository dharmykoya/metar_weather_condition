from django.urls import path
from . import views

urlpatterns = [
    path('', views.metar, name='metar'),
    path('metar/ping', views.ping, name='pinh'),
    path('metar/info', views.metar, name='metar'),

]
