from django.urls import path

from . import views

urlpatterns = [
    path("", views.search_form_index, name="search_form_index"),
    path("search/", views.search_view, name="search_view"),
    path(
        "question/<int:question_id>/",
        views.question_detail_view,
        name="question_detail",
    ),
]
