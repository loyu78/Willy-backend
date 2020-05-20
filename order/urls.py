from django.urls import path

from .views import (
		CartView,
		RemoveProduct,
	)

urlpatterns = [
	path('/cart', CartView.as_view()),
	path('/cart/remove', RemoveProduct.as_view()),
]
