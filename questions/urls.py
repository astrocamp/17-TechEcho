# questions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.index, name="index"
    ),  # Maps the root URL of the questions app to the index view
]
