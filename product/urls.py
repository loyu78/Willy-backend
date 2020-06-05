from django.urls import path

from .views import(
    ProductView,
    ProductDetailView,
    ReviewList,
    ReviewDetail,
)

urlpatterns = [
    path('/review', ReviewList.as_view()),
    path('/review/<int:review_id>', ReviewDetail.as_view()),
    path('', ProductView.as_view()),
    path('/<str:products_id>', ProductDetailView.as_view()),
]
