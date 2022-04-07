from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Device, SensorValue
from .forms import DeviceForm
from .helpers import take_action, send_data_to_thingSpeak


def index(request):
    if request.user.is_authenticated:
        devices = Device.objects.filter(user=request.user)
        context = {"devices": devices}
        return render(request, "monitor/index.html", context)
    return render(request, "monitor/index_nouser.html")


def about(request):
    return render(request, "about.html")


@login_required
def create_device(request):
    form = DeviceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            new_device_id = Device.objects.all().count()
            new_device_id += 1

            instance.unique_id = new_device_id
            instance.user = request.user
            instance.save()
            messages.info(request, f"New Device Successfully Created!")
            return redirect("index")
        messages.error(request, "Form is Invalid! ,Kindly Re-Submit")
    return render(request, "monitor/create_device.html", {"form": form})


@login_required
def sensor_data(request, id):
    device_obj = get_object_or_404(Device, pk=id)
    data = device_obj.data.all()
    context = {"device_obj": device_obj, "data": data}
    return render(request, "monitor/device_detail.html", context=context)


@csrf_exempt
def get_current_data(request, id):
    if request.method == "GET":
        device_obj = get_object_or_404(Device, pk=id)
        data = device_obj.data.all()[0]
        data = {
            "temperature": data.temperature,
            "humidity": data.humidity,
            "light": data.light,
            "ir": data.ir,
        }
        data['result'] = take_action(data)
        return JsonResponse(data, status=200)
    return HttpResponseNotAllowed()


@csrf_exempt
def receive_sensor_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        device_id = data.get("device_id")
        device_obj = get_object_or_404(Device, unique_id=device_id)

        sensor_obj = SensorValue.objects.create(
            ir=str(data.get("ir")),
            temperature=str(data.get("temperature")),
            humidity=str(data.get("humidity")),
            light=str(data.get("light")),
        )

        data = {
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "light": data.get("light"),
            "ir": data.get("ir"),
        }

        send_data_to_thingSpeak(data)
        result = take_action(data)

        device_obj.data.add(sensor_obj)
        return JsonResponse({"result": result}, status=200)

    return HttpResponseNotAllowed()
