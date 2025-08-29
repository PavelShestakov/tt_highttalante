from django.urls import path
from .views import QuestionAPIviews, AnswerAPIviews

urlpatterns = [
    path('questions/', QuestionAPIviews.as_view()),
    path('questions/<int:id>/', QuestionAPIviews.as_view()),
    path('questions/<int:id>/answers/', AnswerAPIviews.as_view()),
    path('answers/<int:id>/', AnswerAPIviews.as_view()),
]
