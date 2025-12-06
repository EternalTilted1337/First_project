from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rooms


@method_decorator(csrf_exempt, name="dispatch")
class RoomsListView(View):  # Список номеров

    def get(self, request):
        rooms = Rooms.objects.all()
        data = {
            "rooms": [{"room_id": r.id, "description": r.description, "price": r.price} for r in rooms]
        }
        return JsonResponse(data, status=200)

    def post(self, request):
        try:
            body = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Некорректный JSON"}, status=400)
        if "description" not in body:
            return JsonResponse({"error": "Некорртетное имя отеля"}, status=400)
        if "price" not in body:
            return JsonResponse({"error": "Неверно указана цена"}, status=400)
        description = body["description"]
        price = body["price"]
        # return JsonResponse({"rooms": [], "description": description, "price": price})# заглушка
        try:
            price = float(price)
        except (ValueError, TypeError):
            return JsonResponse({"error": "цена должна быть числом"}, status=400)

        room = Rooms.objects.create(description=description, price=price)

        return JsonResponse(
            {"room_id": room.id, "description": room.description, "price": room.price},
            status=201,
        )


@method_decorator(csrf_exempt, name="dispatch")
class RoomsDetailView(View):
    def delete(self, request, room_id):
        try:
            room = Rooms.objects.get(id=room_id)
        except Rooms.DoesNotExist:
            return JsonResponse({'error':'Номер не найден'}, status=404)
        room.delete()
        return JsonResponse({'success': True}, status=200)
