from django.shortcuts import render
import time
from .models import WebSiteCategory
# -------------------------------------------------------------------------------------------------------------------------------
def FindWebsiteCategory(website):
    cats_name = list(WebSiteCategory.objects.values_list('name', flat=True))

    cats = scrap(website.domain, cats_name)

    website.categories.add(*WebSiteCategory.objects.filter(name__in=cats))
    website.save()
# -------------------------------------------------------------------------------------------------------------------------------
def scrap(url,categories):
    time.sleep(5)
    print(f"url: {url}\ncategories: {categories}")
    return categories[:1]