from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Rooms, Booking
import json
import datetime

from django.shortcuts import render
@method_decorator(csrf_exempt, name="dispatch")
class RoomsListView(View):  # Список номеров

    def get(self, request):
        rooms = Rooms.objects.all()
        data = {
            "rooms": [
                {"room_id": r.id, "description": r.description, "price": r.price}
                for r in rooms
]
        }
        return JsonResponse(data, status=200)

    def post(self, request):
        try:
            body = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Некорректный JSON"}, status=400)
        if "description" not in body:
            return JsonResponse({"error": "Некорректное имя отеля"}, status=400)
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
            {"room_id": room.id,
             "description": room.description,
             "price": room.price},
            status=201,
        )


@method_decorator(csrf_exempt, name="dispatch")
class RoomsDetailView(View):
    def delete(self, request, room_id):
        try:
            room = Rooms.objects.get(id=room_id)
        except Rooms.DoesNotExist:
            return JsonResponse({"error": "Номер не найден"}, status=404)
        bookings = Booking.objects.filter(room=room)
        if len(bookings) > 0:
            return JsonResponse({'error':'Нельзя удалить комнату. Комната имеет бронь!'}, status=400)
        room.delete()
        return JsonResponse({"success": True}, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class BookingListView(View):#Список и создание брони
    def get(self, request):
        room_id = request.GET.get("room_id")
        if not room_id:
            return JsonResponse({'error': 'Нужно передать room_id',}, status=400)

        try:
            room = Rooms.objects.get(id=room_id)
        except Rooms.DoesNotExist:
            return JsonResponse({'error':'Номер не найден'}, status=404)

        bookings = Booking.objects.filter(room=room).order_by("date_start")

        data =[ {
            'booking_id': b.id,
            'date_start':b.date_start.strftime('%Y-%m-%d'),
            'date_end': b.date_end.strftime("%Y-%m-%d"),
        } 
        for b in bookings
        ]
        return JsonResponse(data,safe=False,status=200)
    def post(self, request):
        try:
            body = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({'error':'Некорректный JSON'}, status=400)
        error = []
        for field in ('room_id', 'date_start', 'date_end'):
            if field not in body:
                error.append(field)
        if len(error) > 0:
            return JsonResponse({'error':f'Некорректно введен {error}'},status = 400)

        room_id = body["room_id"]
        date_start_str = body["date_start"]
        date_end_str = body["date_end"]
        try:
            room = Rooms.objects.get(id=room_id)
        except Rooms.DoesNotExist:
            return JsonResponse({'error':'Номер не найден'}, status= 404)
        try:
            date_start = datetime.datetime.strptime(date_start_str, "%Y-%m-%d").date()
            date_end = datetime.datetime.strptime(date_end_str, "%Y-%m-%d").date()

        except ValueError:
            return JsonResponse({'error':'Неверный формат даты, нужен YYYY-MM-DD'}, status=400)

        if date_start >= date_end:
            return JsonResponse({'error':'date_start должен быть раньше чем date_end'}, status=400)

        overlapp = Booking.objects.filter(room=room,date_start=date_start,date_end=date_end).exists()
        if overlapp:
            return JsonResponse({'error':'Номер уже забронирован на эти даты'}, status = 400)
        booking = Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
        
        return JsonResponse({'booking_id': booking.id}, status=201)

@method_decorator(csrf_exempt, name="dispatch")
class BookingDetailView(View):#Удаление брони
    def delete(self,request,booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({'error':'Бронь не найдена'}, status=404)
        booking.delete()
        return JsonResponse({"success": True}, status=200)



def index(request):
    return render(request, "index.html")

def rooms(request):
    rooms_qs = Rooms.objects.all()
    return render(request, "list_hotel.html", {"rooms": rooms_qs})