from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_view, name="search_index"),
    path("home/", views.index, name="home_index"),
    path("search/", views.search_view, name="search_view"),
]
