import imp
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),

    #APIs
    path('api/send/',views.receive_sensor_data),
]
