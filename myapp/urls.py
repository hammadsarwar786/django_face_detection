from django.urls import path
from .views import post_data
from .face import post_data2

urlpatterns = [
    path('api/', post_data),
    path('faceapi/', post_data2),
]