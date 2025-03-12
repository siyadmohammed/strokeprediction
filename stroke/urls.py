from django.urls import path
from .views import stroke_prediction_view

urlpatterns = [
    path('', stroke_prediction_view, name='stroke_prediction'),
]
