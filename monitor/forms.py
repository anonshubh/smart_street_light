from django import forms

from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ('user','unique_id','data')