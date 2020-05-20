from django.urls import path

from .views import ReviewList, ReviewDetail

urlpatterns = [
	path('/review', ReviewList.as_view()),
	path('/review/<int:review_id>', ReviewDetail.as_view()),
]
