from django.urls import path

from . import views

app_name = "answers"

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/", views.edit, name="edit"),
    path("delete/", views.delete, name="delete"),
    path("vote/<str:vote_type>/", views.vote, name="vote"),
]
