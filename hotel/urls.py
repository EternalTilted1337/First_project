from django.urls import path

from .views import RoomListView, RoomDetailView, BookingListView, BookingDetailView

urlpatterns = [
    path("", RoomListView.as_view(), name="rooms-list"),
    path("<int:room_id>/", RoomDetailView.as_view(), name="rooms-detail"),
    path("bookings/", BookingListView.as_view(), name="bookings-list-create"),
    path(
        "bookings/<int:booking_id>/",
        BookingDetailView.as_view(),
        name="bookings-detail",
    ),
]
