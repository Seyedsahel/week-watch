from unicodedata import category
from django.contrib import admin
from .models import *

admin.site.register(Website)
admin.site.register(WebSiteCategory)
admin.site.register(HistoryRecord)