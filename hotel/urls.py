
from django.urls import path

from . import views
from .views import Hotel
urlpatterns = [
    #path("", views.index, name="index"),
    path("", Hotel.as_view(), name="hotel"),
]
