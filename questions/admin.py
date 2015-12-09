from django.contrib import admin
from .models import Question
# Register your models here.

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    pass
