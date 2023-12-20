from django.shortcuts import render
import time
from .models import WebSiteCategory
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
# -------------------------------------------------------------------------------------------------------------------------------
def FindWebsiteCategory(website):
    cats_name = list(WebSiteCategory.objects.values_list('name', flat=True))

    cats = scrap(f"https://{website.domain}/", cats_name)
    print(cats)
    
    website.categories.add(*WebSiteCategory.objects.filter(name__in=cats))
    website.save()
# ----------------------------------web scraping---------------------------------------------------------------------------------------------
def scrap(given_url,given_categories):
    url = given_url
    count1=0
    count2=0

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        title_element = soup.find("title")

        if title_element:
            print("onvan site:", title_element.text)
        else:
            print("onsor peyda nshod.")

        meta_tags = soup.find_all("meta")
        category = None

        for tag in meta_tags:
            if tag.get("name") == "category":
                category = tag.get("content")
                break

        if category:
            print("category:", category)
        else:
            count2 +=1
            print("daste bandi peyda nshod",count2)
            
    else:
        count1 +=1
        print("khata dar daryaft web page", response.status_code,count1)

    return title_element