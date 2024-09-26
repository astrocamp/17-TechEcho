from django.contrib import admin

from .models import Question, Votes

admin.site.register(Question)
admin.site.register(Votes)
