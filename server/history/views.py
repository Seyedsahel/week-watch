from email.message import EmailMessage
from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from .models import *
from websites.models import Website,WebSiteCategory
# -------------------------------------------------------------------------------------------------------------------------------
def GetRecord(request):
    if request.method == "POST":
        data = request.POST


        link = data.get("link")
        email = data.get("email")

        if not email:
            return JsonResponse({'message': 'email is empty.'}, status=400)
        
        if not link:
            return JsonResponse({'message': 'link is empty.'}, status=400)

        domain = link.split("/")[2]

        
        try:
            website = Website.objects.get(domain=domain)
        except Website.DoesNotExist:
            website = Website(domain=domain)
            website.save()


        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            user.set_password("12345678")
            user.save()



        new_record = HistoryRecord(
            link = link,
            website = website,
            user = user)

        new_record.save()


        return JsonResponse({'message': 'link recorded.'})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
        
# -------------------------------------------------------------------------------------------------------------------------------
def my_view(request):
    return HttpResponse('Hello world')
