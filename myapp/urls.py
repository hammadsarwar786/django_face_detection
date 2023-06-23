from django.urls import path
from .views import post_data

urlpatterns = [
    path('api/', post_data),
]