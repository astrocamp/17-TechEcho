from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("<int:id>/", views.show, name="show"),
    path("<int:id>/edit/", views.edit, name="edit"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("<int:id>/votes/", views.votes, name="votes"),
]
