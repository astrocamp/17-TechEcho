from django.urls import path

from . import views

app_name = "answers"

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/", views.delete, name="delete"),
    path("upvote/", views.upvote, name="upvote"),
    path("downvote/", views.downvote, name="downvote"),
]
