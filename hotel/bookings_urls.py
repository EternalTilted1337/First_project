from django.urls import path
from .views import BookingListView, BookingDetailView, RoomListView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:booking_id>/', BookingDetailView.as_view(), name='booking-detail'),
]