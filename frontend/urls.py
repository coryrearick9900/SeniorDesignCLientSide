from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('collect', index),
    path('thing', index)
]