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
    def find_keywords(text):
        tokens = word_tokenize(text)
    # حذف کلمات توقفی
        stop_words = set(stopwords.words('english'))  # تنظیم زبان متن مورد نظر خود
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        fdist = FreqDist(filtered_tokens)
        keywords = fdist.most_common(12)  # تعداد کلمات کلیدی 
        return keywords


    url=given_url
    
    title=''
    cleans=[]
    count=0
    junk=['از','به','با','برای','در','هم','و','اگر','همراه','حتما','قطعا','کاملا','است','هست','اره','هستید','دنبال','،','را','لطفا','منتظر','بمانید']
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
            keywords = find_keywords(p_text)
            for keyword in keywords: 
                temp = keyword[0] 
                if temp in junk: 
                    count+=1 
            
                else: 
                    cleans.append(keyword)
    else:
        print(page.status_code)

       

    return cleans