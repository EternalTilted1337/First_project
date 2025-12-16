from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer
from django.shortcuts import render

class RoomListView(APIView):  # Список номеров
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            room = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):
    def delete(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Номер не найден"}, status=status.HTTP_404_NOT_FOUND)
        bookings = Booking.objects.filter(room=room)
        if len(bookings) > 0:
            return Response(
                {"error": "Нельзя удалить комнату. Комната имеет бронь!"}, status=status.HTTP_400_BAD_REQUEST
            )
        room.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)



class BookingListView(APIView):  # Список и создание брони
    def get(self, request):
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response(
                {
                    "error": "Нужно передать room_id",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Номер не найден"}, status=status.HTTP_404_NOT_FOUND)

        bookings = Booking.objects.filter(room=room).order_by("date_start")

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailView(APIView):  # Удаление брони
    def delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Бронь не найдена"}, status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


def index(request):
    return render(request, "index.html")


def rooms(request):
    rooms_qs = Room.objects.all()
    return render(request, "list_hotel.html", {"rooms": rooms_qs})
