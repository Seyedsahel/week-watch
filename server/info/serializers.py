from rest_framework import serializers
from .models import *

class HistorySerializers(serializers.ModelSerializer):
    link = serializers.CharField()
    class Meta:
        model = HistoryRecord
        fields = ['link',]