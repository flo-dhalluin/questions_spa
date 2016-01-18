from django.contrib import admin
from .models import Question
from .models import Answer

class AnswerInline(admin.StackedInline):
    model = Answer

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
