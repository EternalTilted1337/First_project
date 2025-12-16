from django.urls import path
from .views import RoomListView, RoomDetailView

urlpatterns = [
    path('', RoomListView.as_view(), name='rooms-list'),
    path('<int:room_id>/', RoomDetailView.as_view(), name='rooms-detail'),
]