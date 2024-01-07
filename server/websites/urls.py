from django.urls import path
from .views import *

urlpatterns = [
    path('websites/category/',GetWebsiteCategory),
]
