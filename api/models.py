from django.db import models

# Create your models here.
class DataPoint(models.Model):
    value = models.FloatField(null=False, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    running = models.BooleanField(default=False)

    # make constructor that calls that funciton below to gather a data point
        

# function to gather a data point
class RadarReading(models.Model):
    speed = models.FloatField(null=False, default=0)


class SpeedThreshhold(models.Model):
    newSpeed = models.IntegerField(null=False, default=0)
