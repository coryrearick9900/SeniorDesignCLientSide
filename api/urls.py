from django.urls import path
from .views import ChangeSpeedThreshhold, DataPointView, GetDataPoint, GetLastSpeed, GetSpeedThreshhold

urlpatterns = [
    path('home', DataPointView.as_view()),
    path('getSpeed', GetDataPoint.as_view()),
    path('getLastReading', GetLastSpeed.as_view()),
    path('changeSpeedThreshhold', ChangeSpeedThreshhold.as_view()),
    path('getSpeedThreshhold', GetSpeedThreshhold.as_view())
]