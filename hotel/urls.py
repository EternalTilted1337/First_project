
from django.urls import path

from . import views
from .views import RoomsListView, RoomsDetailView

urlpatterns = [
    path("", RoomsListView.as_view(), name = "rooms"),
    path('<int:room_id>/', RoomsDetailView.as_view(), name = "rooms-detail"),
]
