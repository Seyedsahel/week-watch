from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from .models import *
from websites.models import Website,WebSiteCategory
from websites.views import FindWebsiteCategory
import threading
from django.db.models import ExpressionWrapper, F, DurationField, Sum
from datetime import datetime
# -------------------------------------------------------------------------------------------------------------------------------
def GetRecord(request):
    print("---------------------------------")
    if request.method == "POST":
        data = request.POST
        print(data)


        link = data.get("link")
        email = data.get("email").lower()
        action = data.get("action")

        if not email:
            return JsonResponse({'message': 'email is empty.'}, status=400)
        
        if not link:
            return JsonResponse({'message': 'link is empty.'}, status=400)

        try:
            domain = link.split("/")[2]
        except IndexError:
            if(link == ""):
                return JsonResponse({'message': 'link is empty.'}, status=400)
            else:
                return JsonResponse({'message': 'link not True.'}, status=400)

        
        try:
            website = Website.objects.get(domain=domain)
        except Website.DoesNotExist:
            website = Website(domain=domain)
            website.save()

        if(website.categories.all().count() == 0):
            thread = threading.Thread(target=FindWebsiteCategory, kwargs={'website': website,})
            thread.start()
            pass



        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            user.set_password("12345678")
            user.save()


        if(action == 'create'):
            new_record = HistoryRecord(
            link = link,
            website = website,
            user = user)

            new_record.save()
        elif(action == 'updated'):
            try:
                record = HistoryRecord.objects.filter(user=user).order_by('-id').first()
            except HistoryRecord.DoesNotExist:
                return JsonResponse({'message': 'record not exist.'}, status=400)


            if(record == None):
                record = HistoryRecord(
                link = link,
                website = website,
                user = user)
            
            if(record.link != link):
                new_record = HistoryRecord(
                    link = link,
                    website = website,
                    user = user)

                new_record.save()
                record.next_record = new_record
                record.closed = datetime.now()
            record.save()

        else:
            try:
                record = HistoryRecord.objects.filter(link=link,user=user)
            except HistoryRecord.DoesNotExist:
                return JsonResponse({'message': 'record not exist.'}, status=400)



        return JsonResponse({'message': 'link recorded.'})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
#-------------------------------------------------------------------------------------------------------------------------------
def get_hours_on_category_websites(request):
    if request.method == "POST":
        data = request.POST
        print(data)


        category_name = data.get("category_name")
        email = data.get("email").lower()

        if not email:
            return JsonResponse({'message': 'email is empty.'}, status=400)
        
        if not category_name:
            return JsonResponse({'message': 'category_name is empty.'}, status=400)


        if(email != request.user.email and not request.user.is_admin):
            return JsonResponse({'message': 'not allowed!'}, status=400)

    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user not found!'}, status=404)
        
        
        try:
            category = WebSiteCategory.objects.get(name=category_name)
        except Website.DoesNotExist:
            return JsonResponse({'message': 'category not found!'}, status=404)

        websites = category.websites.all()

        print(websites)
        duration = 0

        data = []

        for website in websites:
            duration = HistoryRecord.objects.filter(user=user, website=website).aggregate(
                total_duration=Sum(
                    ExpressionWrapper(F('closed') - F('created'), output_field=DurationField())
                )
            )
            
            total_duration = duration['total_duration']
            
            if total_duration is not None:
                hours = total_duration.seconds // 3600
                minutes = (total_duration.seconds % 3600) // 60
                seconds = total_duration.seconds % 60
                
                website_data = {
                    'website': website.domain,
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds,
                }
                
                data.append(website_data)

        return JsonResponse({'message': data})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
#-------------------------------------------------------------------------------------------------------------------------------
def get_hours_on_website(request):
    if request.method == "POST":
        data = request.POST
        print(data)


        domain = data.get("domain")
        email = data.get("email").lower()

        if not email:
            return JsonResponse({'message': 'email is empty.'}, status=400)
        
        if not domain:
            return JsonResponse({'message': 'domain is empty.'}, status=400)


        if(email != request.user.email and not request.user.is_admin):
            return JsonResponse({'message': 'not allowed!'}, status=400)

    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user not found!'}, status=404)
        

        
        try:
            website = Website.objects.get(domain=domain)
        except Website.DoesNotExist:
            return JsonResponse({'message': 'website not found!'}, status=404)

        duration = HistoryRecord.objects.filter(user=user, website=website).aggregate(
            total_duration=Sum(
                ExpressionWrapper(F('closed') - F('created'), output_field=DurationField())
            )
        )



        total_duration = duration['total_duration']
        hours = total_duration.seconds // 3600
        minutes = (total_duration.seconds % 3600) // 60
        seconds = total_duration.seconds % 60

        data = {
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
        }

        return JsonResponse({'message': data})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
#-------------------------------------------------------------------------------------------------------------------------------
def get_hours_on_category(request):
    if request.method == "POST":
        data = request.POST
        print(data)


        category_name = data.get("category_name")
        email = data.get("email").lower()

        if not email:
            return JsonResponse({'message': 'email is empty.'}, status=400)
        
        if not category_name:
            return JsonResponse({'message': 'category_name is empty.'}, status=400)


        if(email != request.user.email and not request.user.is_admin):
            return JsonResponse({'message': 'not allowed!'}, status=400)

    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user not found!'}, status=404)
        
        
        try:
            category = WebSiteCategory.objects.get(name=category_name)
        except Website.DoesNotExist:
            return JsonResponse({'message': 'category not found!'}, status=404)

        websites = category.websites.all()

        cat_data = {
                    'name': category_name,
                    'hours': 0,
                    'minutes': 0,
                    'seconds': 0,
        }

        for website in websites:
            duration = HistoryRecord.objects.filter(user=user, website=website).aggregate(
                total_duration=Sum(
                    ExpressionWrapper(F('closed') - F('created'), output_field=DurationField())
                )
            )
            
            total_duration = duration['total_duration']
            
            if total_duration is not None:
                hours = total_duration.seconds // 3600
                minutes = (total_duration.seconds % 3600) // 60
                seconds = total_duration.seconds % 60
                
                
                cat_data['hours'] += hours
                cat_data['minutes'] += minutes
                cat_data['seconds'] += seconds

        return JsonResponse({'message': cat_data})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
#-------------------------------------------------------------------------------------------------------------------------------
