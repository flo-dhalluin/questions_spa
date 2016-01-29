from django.conf.urls import include, url, patterns
#from rest_framework.urlpatterns import format_suffix_patterns
from .views import QuestionListView, QuestionDetailView, AnswerCreateView


urlpatterns = patterns('',
                       url(r'^$', QuestionListView.as_view(), name='question-list'),
                       url(r'^question/(?P<slug>[-_\w]+)$', QuestionDetailView.as_view(), name='question-detail'),
                       url(r'^question/(?P<slug>[-_\w]+)/answer/$', AnswerCreateView.as_view(), name='create-answer'),
                       )

#urlpatterns = format_suffix_patterns(urlpatterns)
