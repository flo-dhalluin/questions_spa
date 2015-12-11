from django.conf.urls import include, url, patterns
#from rest_framework.urlpatterns import format_suffix_patterns
from .views import QuestionListView


urlpatterns = patterns('',
                       url(r'^$', QuestionListView.as_view(), name='question-list'),
                       )

#urlpatterns = format_suffix_patterns(urlpatterns)
