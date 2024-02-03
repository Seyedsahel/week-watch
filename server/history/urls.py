from django.urls import path
from .views import *

urlpatterns = [
    path('record/',GetRecord),
    path('record/onWebsite/',get_hours_on_website),
    path('record/onCategoryWebsites/',get_hours_on_category_websites),
    path('record/onCategory/',get_hours_on_category),
    path('website/views/',WebsiteVisitsOnWeekAPI.as_view(),name="website_views"),
    path('website/views/unique/',WebsiteUniqueVisitsOnWeekAPI.as_view(),name="website_views_unique"),
]
