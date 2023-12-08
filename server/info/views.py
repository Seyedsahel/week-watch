from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
def GetRecord(request):
    if request.method == "POST":
        data = request.POST

        link = data.get("link")
        domain = link.split("/")[2]


        
        try:
            website = Website.objects.get(domain=domain)
        except Website.DoesNotExist:
            website = Website(domain=domain)
            website.save()


        email = data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user not found.'}, status=403) 



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
