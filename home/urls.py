from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("nav", views.nav, name="nav"), 開發用
]
