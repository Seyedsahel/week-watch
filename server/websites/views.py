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
# -------------------------------------------------------------------------------------------------------------------------------
def scrap(given_url,given_categories):
    print(given_url)
    def find_keywords(text):
        tokens = word_tokenize(text)
    # حذف کلمات توقفی
        stop_words = set(stopwords.words('english'))  # تنظیم زبان متن مورد نظر خود
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        fdist = FreqDist(filtered_tokens)
        keywords = fdist.most_common(12)  # تعداد کلمات کلیدی 
        return keywords

    def find_paragraph(paragraph,soup):
        junk=['از','به','با','برای','در','هم','و','اگر','همراه','حتما','قطعا','کاملا','است','هست','اره','هستید','دنبال','،','را','لطفا','منتظر','بمانید']
        cleans=[]
        count=0
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
                    # print(keyword[0])
                    # print(f"count:{count}")
        print(f"count:{count}")           
        return cleans
        

    def find_category():
        url=given_url
        main_keyword=[]
        title=''
        page=requests.get(url)

        if page.status_code == 200:
            soup =BeautifulSoup(page.text,"html.parser") #گرفتن صفحه 
            try:
                title = soup.find('title').text
            except AttributeError:
                print("سایت احمقش تگ تایتل نداره")
                #............... پیدا کردن کلمات کلیدی.......................
            paragraphs = soup.find_all('p') #پیدا کردن پاراگراف ها
            for paragraph in paragraphs:
                main_keyword=find_paragraph(paragraph,soup)
                if len(main_keyword)>2:
                    break
        else:
            print(page.status_code)
        #پیدا کن این لیست کتگوری رو بر اساس تایتل و کلمات کلیدی
        categories=['فروشگاهی','اجتماعی','آموزشی']

        return main_keyword

#چک کردن کتگوری پیدا شده با کتگوری داده شده
    found_categories=find_category()
    final_categories=[]
    for cat in found_categories:
        if cat[0] in given_categories:
            final_categories.append(cat[0])

    return final_categories