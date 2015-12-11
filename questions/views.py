from rest_framework import generics
from .serializers import QuestionSerializer
from .models import Question

class QuestionListView(generics.ListCreateAPIView):
    model = Question
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
