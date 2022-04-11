from rest_framework import serializers
from .models import DataPoint, RadarReading, SpeedThreshhold

class DataPointSeralizer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('id', 'value', 'timestamp')

class RadarSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadarReading
        fields = ('speed')

class SpeedThreshholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedThreshhold
        fields = ('newSpeed', )