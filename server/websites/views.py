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
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from langdetect import detect

def scrap(given_url,given_categories):
    def find_keywords_e(text):
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))  # تنظیم زبان متن مورد نظر خود
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        fdist = FreqDist(filtered_tokens)
        keywords = fdist.most_common(12)  # تعداد کلمات کلیدی 
        return keywords
    


    def find_keywords(soup):
        junk = ['از', 'به', 'با', 'برای', 'در', 'هم', 'و','اگر', 'هست', 'هستید', 'دنبال', '،', 'را',
                   'منتظر', 'بمانید', 'کردن', 'بودن', 'داشتن','شدن', 'رفتن', 'آمدن', 'بسیار', 'خیلی',
                       'کاملاً', 'تماماً', 'همیشه', 'همانا', 'این', 'آن', 'اینها', 'آنها', 'بار', 'مرتبه', 'دفعه',
                         'فاصله', 'نقطه', 'خط', 'تا', 'باشه', 'بوده', 'باشد','باشید', 'باشند', 'دارد', 'داره', 'داشته',
                             'داشتند', 'داشتید', 'داشتیم', 'هستم', 'هستی', 'هستیم','هستند', 'خیلی‌ها', 'بسیاری', 'بیشتر', 'کمتر', 'تعدادی', 'برخی', 'همه',
                                 'هیچ', 'کسی', 'چند', 'چیزی', 'بیش', 'کم', 'زیاد', 'کمی', 'عمدتا', 'اکثراً', 'به‌طور', 'بنابراین',
                                   'بطور', 'بنابر', 'ناچار', 'علاوه', 'به‌علاوه', 'اصولاً', 'عموماً', 'کلیاً', 'غالباً', 'نسبتاً', 'به‌طورکلی', 'از', 'به', 'با', 'برای', 'در', 'هم', 'و', 'اگر', 'هست', 'هستید',
                                     'دنبال', '،', 'را', 'منتظر', 'بمانید', 'کردن', 'بودن', 'داشتن', 'شدن', 'رفتن', 'آمدن', 'بسیار', 'خیلی', 'کاملاً', 'تماماً', 'همیشه', 'همانا', 'این', 'آن', 'اینها', 'آنها', 'بار', 'مرتبه', 'دفعه', 'فاصله', 'نقطه', 'خط', 'تا', 'باشه', 'بوده', 'باشد', 'باشید', 'باشند', 'دارد', 'داره', 'داشته', 
                                     'داشتند', 'داشتید', 'داشتیم', 'هستم', 'هستی', 'هستیم', 'هستند', 'خیلی‌ها', 'بسیاری', 'بیشتر', 'کمتر', 'تعدادی', 'برخی', 'همه', 'هیچ', 'کسی', 'چند', 'چیزی', 'بیش', 'کم', 'زیاد', 'کمی', 'عمدتا', 'اکثراً', 'به‌طور', 'بنابراین', 'بطور', 'بنابر']
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
            if temp in junk: 
                count+=1 
            else: 
                cleans.append(keyword)           
        return cleans
        

    def find_category():
        cats_dict_p = {
        'فروشگاهی': ['خرید', 'فروش', 'نمایندگی', 'محصول', 'تخفیف', 'خرید اینترنتی', 'پرداخت', 'تحویل', 'قیمت', 'مغازه'],
        'اداری': ['ثبت', 'اطلاعات', 'مستندات', 'کارمندان', 'مدیریت', 'امور', 'دفتر', 'قرارداد', 'کمیسیون', 'سازمان'],
        'آموزشی': ['دانشجو', 'دانشگاه', 'درس', 'استاد', 'آموزش', 'کلاس', 'دبیرخانه', 'پژوهش', 'کتابخانه', 'آزمون','تمرین','دوره','کتاب'],
        'سرگرمی': ['بازی', 'فیلم', 'موسیقی', 'کنسرت', 'تئاتر', 'سینما', 'هنر', 'تفریح', 'گیم', 'هیجان','کتاب'],
        'اجتماعی': ['جمعیت', 'اعضا', 'اجتماع', 'مراسم', 'جشن', 'تشریفات', 'همایش', 'سخنرانی', 'مردم', 'رهبر'],
        'خبری': ['اخبار', 'روزنامه', 'خبرگزاری', 'سیاسی', 'اقتصادی', 'فرهنگی', 'ورزشی', 'بین‌المللی', 'تکنولوژی', 'علمی']
        }
        cats_dict_e = {
        'فروشگاهی': ['shopping', 'sale', 'agency', 'product', 'discount', 'online shopping', 'payment', 'delivery', 'price', 'store'],
        'اداری': ['registration', 'information', 'documents', 'employees', 'management', 'affairs', 'office', 'contract', 'commission', 'organization'],
        'آموزشی': ['student', 'university', 'lesson', 'professor', 'education', 'class', 'secretariat', 'research', 'library', 'exam', 'exercise', 'course'],
        'سرگرمی': ['game', 'movie', 'music', 'concert', 'theater', 'cinema', 'art', 'entertainment', 'gaming', 'excitement'],
        'اجتماعی': ['community', 'members', 'society', 'ceremony', 'celebration', 'event', 'speech', 'people', 'leader'],
        'خبری': ['news', 'newspaper', 'news agency', 'political', 'economic', 'cultural', 'sports', 'international', 'technology', 'scientific']
        }
        
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
                    for key in cats_dict_p:
                        values = cats_dict_p[key]
                        for value in values:
                            for k in main_keyword:
                                if value in k[0]:
                                    final_categories.append(key)
                        
        else:
            for key in cats_dict_e:
                        values = cats_dict_p[key]
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
    