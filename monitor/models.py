from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Device(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    unique_id = models.PositiveIntegerField()
    lat = models.CharField(max_length=20)
    long = models.CharField(max_length=20)
    data = models.ManyToManyField('SensorValue')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.unique_id)

class SensorValue(models.Model):
    temperature = models.CharField(max_length=21)
    humidity = models.CharField(max_length=21)
    ir = models.CharField(max_length=21)
    light = models.CharField(max_length=21)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

