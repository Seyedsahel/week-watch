from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from .models import HistoryRecord
# -------------------------------------------------------------------------------------------------------------------------------
def GetRecord(request):
    if request.method == "POST":

        new_record = HistoryRecord(link=str(request.POST.get("link")))
        new_record.save()


        return JsonResponse({'message': 'link recorded.'})
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)
        
# -------------------------------------------------------------------------------------------------------------------------------
def my_view(request):
    return HttpResponse('Hello world')
