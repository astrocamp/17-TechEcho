from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("teachers/", include("teachers.urls")),
    path("questions/", include("questions.urls")),
    path("users/", include("users.urls")),
    path("questions/<int:id>/answers/", include("answers.urls")),
    path("payments/", include("payments.urls")),
    path("accounts/", include("allauth.urls")),
    path("chat/", include("chat.urls")),
    path("appointments/", include("appointments.urls")),
    path("blogs/", include("blogs.urls")),
    path("markdownx/", include("markdownx.urls")),
]
