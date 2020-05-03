from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tweet_item import views

urlpatterns = [
    path('', views.TweetItemList.as_view()),
    # path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
