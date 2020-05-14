import json

from django.views import View
from django.http import  HttpResponse, JsonResponse

from .models import Home

class HomeView(View):
    def get(self, request):
        home_list = Home.objects.all().values()
        return JsonResponse({'home_list':list(home_list)}, status=200)

