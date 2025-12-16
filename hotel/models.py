from django.db import models
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

class Room(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id} : {self.description[:20]}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.date_start and self.date_end:
            if self.date_start >= self.date_end:
                raise DjangoValidationError('date_end', 'Дата окончания бронирования должна быть позже даты начала')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for Room {self.room_id} from {self.date_start} to {self.date_end}"