from django.urls import path
from .views      import SurveyView, SurveyResultView

urlpatterns = [
    path('', SurveyView.as_view()),
    path('/result',SurveyResultView.as_view()),
]

