from rest_framework import generics
from .serializers import QuestionSerializer
from .serializers import QuestionWithAnswersSerializer
from .models import Question

class QuestionListView(generics.ListCreateAPIView):
    model = Question
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionWithAnswersSerializer
    # by default, the "RetrieveView" uses pk field to get one element
    # let's use slug instead
    lookup_field = 'slug'
