from django.contrib import admin
from django.urls import path

from measurement.views import SensorsView, IdSensorView, MeasurementView

urlpatterns = [
    path("sensors/", SensorsView.as_view()),
    path("sensors/<pk>/", IdSensorView.as_view()),
    path("measurements/", MeasurementView.as_view()),
]
