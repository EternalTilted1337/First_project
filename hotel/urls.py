from django.urls import path

from .views import RoomsListView, RoomsDetailView, BookingListView, BookingDetailView

urlpatterns = [
    path("", RoomsListView.as_view(), name="rooms-list"),
    path("<int:room_id>/", RoomsDetailView.as_view(), name="rooms-detail"),
    path("bookings/list/", BookingListView.as_view(), name="bookings-list"),
    path("bookings/create/", BookingListView.as_view(), name="bookings-create"),
    path(
        "bookings/<int:booking_id>/",
        BookingDetailView.as_view(),
        name="bookings-detail",
    ),
    path(
        "delete/<int:booking_id>/", BookingDetailView.as_view(), name="bookings-delete"
    ),
]
