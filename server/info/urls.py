from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('record/',GetRecord),
     path('fuck/',my_view),
]
