from django.urls import path

from .views import (
		CartView,
		RemoveProducts,
		RemoveProduct,
	)

urlpatterns = [
	path('/cart', CartView.as_view()),
	path('/cart/remove', RemoveProducts.as_view()),
	path('/cart/remove/<int:product_id>', RemoveProduct.as_view()),
]
