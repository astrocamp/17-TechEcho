from django.urls import path

from . import views

app_name = "blogs"

urlpatterns = [
    path("", views.index, name="index"),
    path("article/<int:pk>", views.show, name="show"),
    path("article/new/", views.new, name="new"),
    path("article/<int:pk>/edit/", views.edit, name="edit"),
    path("article/<int:pk>/delete/", views.delete, name="delete"),
]
