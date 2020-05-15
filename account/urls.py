from django.urls import path

from .views import PointProductList, PointProductDetail

urlpatterns = [
	path('/gift', PointProductList.as_view()),
	path('/gift/<int:product_id>', PointProductDetail.as_view()),
]
