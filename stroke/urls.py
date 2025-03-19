from django.urls import path
from .views import stroke_prediction_view,login_view,logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('stroke/', stroke_prediction_view, name='stroke_prediction'),
]
