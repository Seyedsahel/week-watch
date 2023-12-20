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
    url=given_url
    
    title=''
    page=requests.get(url)

    if page.status_code == 200:
        soup =BeautifulSoup(page.text,"html.parser") #گرفتن صفحه 
        try:
            title = soup.find('title').text
        except AttributeError:
            print("سایت احمقش تگ تایتل نداره")
    paragraphs = soup.find_all('p') #پیدا کردن پاراگراف ها
    for paragraph in paragraphs:
        class_name = paragraph.get('class') #گرفتن اسم کلاس های تگ p
        if class_name != 'None':
            p_text=soup.find('p',class_=class_name).text#پیدا کردن متن توی تگ
        
    else:
        print(page.status_code)

    return p_text