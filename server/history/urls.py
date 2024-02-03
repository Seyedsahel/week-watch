from django.urls import path
from .views import *

urlpatterns = [
    path('record/',GetRecord),
    path('record/onWebsite/',get_hours_on_website),
]
