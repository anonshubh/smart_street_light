from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.exceptions import ValidationError,PermissionDenied
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Device,SensorValue
from .helpers import take_action,send_data_to_thingSpeak

def index(request):
    if(request.user.is_authenticated):
        devices = Device.objects.filter(user=request.user)
        context = {
            'devices':devices
        }
        return render(request, "monitor/index.html",context)
    return render(request, "monitor/index_nouser.html")

def about(request):
    return render(request, "monitor/about.html")


@csrf_exempt
def receive_sensor_data(request):
    if request.method == "POST":
        data =  json.loads(request.body)
        device_id = data.get('device_id')
        device_obj = get_object_or_404(Device,unique_id=device_id)

        sensor_obj = SensorValue.objects.create(
            ir = str(data.get('ir')),
            temperature = str(data.get('temperature')),
            humidity = str(data.get('humidity')),
            light = str(data.get('light'))
        )

        data = {
            'temperature':data.get('temperature'),
            'humidity':data.get('humidity'),
            'light':data.get('light'),
            'ir':data.get('ir'),
        }

        send_data_to_thingSpeak(data)
        result = take_action(data)

        device_obj.data.add(sensor_obj)
        return JsonResponse({"result":result},status=200)

    return HttpResponseNotAllowed()
