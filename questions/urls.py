from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path("", views.index, name="views"),
    path("new", views.new, name="new"),
    path("<int:id>", views.show, name="show"),
    path("<int:id>", views.edit, name="edit"),
]
