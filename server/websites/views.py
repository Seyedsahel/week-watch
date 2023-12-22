from django.shortcuts import render
import time
from .models import WebSiteCategory
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from langdetect import detect
import json
# -------------------------------------------------------------------------------------------------------------------------------
def FindWebsiteCategory(website):
    cats_name = list(WebSiteCategory.objects.values_list('name', flat=True))

    cats = scrape(f"https://{website.domain}/", cats_name)
    print(cats)
    if len(cats)==0:
        links=find_link(f"https://{website.domain}/")
        for i in links:
            cats=scrape(i)
            if len(cats)!=0:
                break
    website.categories.add(*WebSiteCategory.objects.filter(name__in=cats))
    website.save()
# ----------------------------------web scraping---------------------------------------------------------------------------------------------
def find_link(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        http_links = []  
        for link in links:
            link_url = link.get('href')
            if link_url and link_url.startswith('http'):
                http_links.append(link_url)
        return http_links
    
def scrape(given_url,given_categories):
    with open('data.json', 'r') as file:
        data = json.load(file)

    loaded_cats_dict_p = data['cats_dict_p']
    loaded_cats_dict_e = data['cats_dict_e']
    loaded_junk = data['junk']
    def find_keywords_e(text):
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))  # تنظیم زبان متن مورد نظر خود
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        fdist = FreqDist(filtered_tokens)
        keywords = fdist.most_common(12)  # تعداد کلمات کلیدی 
        return keywords
    


    def find_keywords(soup):
       
        cleans=[]
        count=0
        status=0
        p_text=""
        title = soup.find('title')
        if title :
            title=title.text
            p_text=p_text+title+","
        h1 = soup.find("h1")
        if h1 :
            h1=h1.text
            p_text=p_text+h1+","
            status+=1
        h2 = soup.find("h2")
        if h2 :
            h2=h2.text
            p_text=p_text+h2+","
            status+=1
        h3 = soup.find("h3")
        if h3 :
            h3=h3.text
            p_text=p_text+h3+","
            status+=1
        strong = soup.find("strong")
        if strong :
            strong=strong.text
            p_text=p_text+strong
            status+=1
        print(p_text)
        if status >=2 :
            keywords = find_keywords_e(p_text)
            
        else:
            paragraphs = soup.find_all('p') #پیدا کردن پاراگراف ها
            for paragraph in paragraphs:
                class_name = paragraph.get('class') #گرفتن اسم کلاس های تگ p
                if class_name != 'None':
                    p_text=soup.find('p',class_=class_name).text#پیدا کردن متن توی تگ
                
                keywords = find_keywords_e(p_text)
            
                if len(keywords)>2:
                    break
            
            
            
        for keyword in keywords: 
            temp = keyword[0] 
            if temp in loaded_junk: 
                count+=1 
            else: 
                cleans.append(keyword)           
        return cleans
        

    def find_category():
        
        
        main_keyword=[]
        final_categories=[]
        page=requests.get(given_url)

        if page.status_code == 200:
            soup =BeautifulSoup(page.text,"html.parser") #گرفتن صفحه 
                #............... پیدا کردن کلمات کلیدی.......................
            main_keyword=find_keywords(soup)
            print(main_keyword)
            
        else:
            print(page.status_code)
        word=main_keyword[0]
        detected_lan = detect(word[0])
        if detected_lan == 'fa':
                    for key in loaded_cats_dict_p:
                        values = loaded_cats_dict_p[key]
                        for value in values:
                            for k in main_keyword:
                                if value in k[0]:
                                    final_categories.append(key)
                        
        else:
            for key in loaded_cats_dict_e:
                        values = loaded_cats_dict_e[key]
                        for value in values:
                            for k in main_keyword:
                                if value in k[0]:
                                    final_categories.append(key)

        return final_categories


    found_categories=find_category()
    final_categories=[]
    for cat in found_categories:
        if cat[0] in given_categories:
            final_categories.append(cat[0])

    return final_categories