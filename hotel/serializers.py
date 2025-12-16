from rest_framework import serializers
from .models import Room, Booking
from django.core.exceptions import ValidationError as DjangoValidationError

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','description','price']
        read_only_fields = ['id']

class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(
        queryset = Room.objects.all(),
        source='room',
        label='ID комнаты',
    )
    class Meta:
        model = Booking
        fields = ['id','room_id', 'date_start', 'date_end']
        read_only_fields = ['id']

    def validate(self, data):
        try:
            instance = Booking(**data)
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        room = data['room']
        date_start = data['date_start']
        date_end = data['date_end']

        overlapp = Booking.objects.filter(room=room, date_start__lt=date_end, date_end__gt=date_start)
        if overlapp.exists():
            raise serializers.ValidationError(
                {'non_field_errors':'Номер уже забронирован на эти даты'}
            )

        return data
