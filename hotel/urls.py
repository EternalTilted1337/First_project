
from django.urls import path

from . import views
from .views import RoomsListView
urlpatterns = [
    path("", RoomsListView.as_view(), name = "rooms"),
]
