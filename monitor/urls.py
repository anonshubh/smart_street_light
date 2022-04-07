from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("create-device/", views.create_device, name="create-device"),
    path("device-details/<int:id>/", views.sensor_data, name="device-detail"),

    #APIs
    path('api/send/',views.receive_sensor_data),
    path('api/get-current/<int:id>/',views.get_current_data),
]
