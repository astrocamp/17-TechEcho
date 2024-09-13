from django.urls import path

from . import views

app_name = "blogs"

urlpatterns = [
    path('', views.article_list, name='articles_index'),  # Updated to match articles_index.html
    path('article/<int:pk>', views.article_detail, name='articles_show'),  # Updated to match articles_show.html
    path('article/new/', views.article_create, name='articles_new'),  # Updated to match articles_new.html
    path('article/<int:pk>/edit/', views.article_update, name='articles_edit'),  # Updated to match articles_edit.html
    path('article/<int:pk>/delete/', views.article_delete, name='articles_delete'),  # Updated to match articles_delete.html
]