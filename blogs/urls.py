from django.urls import path

from . import views

app_name = "blogs"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.show, name="show"),
    path("drafts/", views.user_drafts, name="user_drafts"),
    path("new/", views.new, name="new"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("image_upload/", views.image_upload, name="image_upload"),
]
