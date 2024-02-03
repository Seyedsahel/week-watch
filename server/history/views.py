from email.message import EmailMessage
from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from .models import *
from websites.models import Website,WebSiteCategory
from websites.views import FindWebsiteCategory
import threading
import datetime
# -------------------------------------------------------------------------------------------------------------------------------
def GetRecord(request):
    print("---------------------------------")
    if request.method == "POST":
        data = request.POST
        print(data)


        link = data.get("link")
        email = data.get("email")
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

            
            if(record.link != link):
                new_record = HistoryRecord(
                    link = link,
                    website = website,
                    user = user)

                new_record.save()
                record.next_record = new_record
            record.save()

        else:
            try:
                record = HistoryRecord.objects.filter(link=link,user=user)
            except HistoryRecord.DoesNotExist:
                return JsonResponse({'message': 'record not exist.'}, status=400)
            
            

        


        return JsonResponse({'message': 'link recorded.'})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
# -------------------------------------------------------------------------------------------------------------------------------
# def get_hours_on_website(request):
#     if request.method == "POST":
#         data = request.POST
#         print(data)


#         link = data.get("link")
#         email = data.get("email")

#         if not email:
#             return JsonResponse({'message': 'email is empty.'}, status=400)
        
#         if not link:
#             return JsonResponse({'message': 'link is empty.'}, status=400)

    
#         try:
#             domain = link.split("/")[2]
#         except IndexError:
#             if(link == ""):
#                 return JsonResponse({'message': 'link is empty.'}, status=400)
#             else:
#                 return JsonResponse({'message': 'link not True.'}, status=400)

        
#         try:
#             website = Website.objects.get(domain=domain)
#         except Website.DoesNotExist:
#             website = Website(domain=domain)
#             website.save()

#         if(website.categories.all().count() == 0):
#             thread = threading.Thread(target=FindWebsiteCategory, kwargs={'website': website,})
#             thread.start()
#             pass



#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             user = User(email=email)
#             user.set_password("12345678")
#             user.save()


#         if(action == 'create'):
#             new_record = HistoryRecord(
#             link = link,
#             website = website,
#             user = user)

#             new_record.save()
#         elif(action == 'updated'):
#             try:
#                 record = HistoryRecord.objects.filter(user=user).order_by('-id').first()
#             except HistoryRecord.DoesNotExist:
#                 return JsonResponse({'message': 'record not exist.'}, status=400)

            
#             if(record.link != link):
#                 new_record = HistoryRecord(
#                     link = link,
#                     website = website,
#                     user = user)

#                 new_record.save()
#                 record.next_record = new_record
#             record.save()

#         else:
#             try:
#                 record = HistoryRecord.objects.filter(link=link,user=user)
#             except HistoryRecord.DoesNotExist:
#                 return JsonResponse({'message': 'record not exist.'}, status=400)
            
            

        


#         return JsonResponse({'message': 'link recorded.'})
#     else:
#         return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)