from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

from rest_framework.relations import method_overridden


# @method_decorator(csrf_exempt, name="dispatch")
# class Hotel(View):
#     def get(self, request):
#         return HttpResponse("HELLO, CLOWN")
#
#     def post(self, request):
#         return HttpResponse("bb, doter")

@method_decorator(csrf_exempt, name="dispatch")
class RoomsListView(View):#Список номеров
    def get(self, request):

        data = {
            'rooms':[],#Сюда буду коннектит бд и выводить номера отелей
        }
        return JsonResponse(data,status=200)

    def post(self, request):
        try:
            body = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        if 'description' not in body:
            return JsonResponse({'error': "Некорртетное имя отеля"}, status=400)
        if 'price' not in body:
            return JsonResponse({"error" : "Неверно указана цена"}, status=400)
        description = body['description']
        price = body['price']
        return JsonResponse({'rooms':[], 'description':description, 'price':price})

