import json
import uuid

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Sum
from django.db.models import Count

from .models          import Order, Cart
from product.models   import Product
from user.models      import User
from user.utils       import sign_in_auth

class CartView(View):
	@sign_in_auth
	def post(self, request):
		data       = json.loads(request.body)
		product_id = data.get( 'product_id' )

        if product_id:
			product = Product.objects.get(id = product_id)
			user    = request.user

			if Order.objects.filter(user_id=user.id, order_status_id=1).exists():
				order_id = Order.objects.get(user_id=user.id).id
			else:
				Order.objects.create(
					user_id = User.objects.get(id=user.id).id,
					order_status_id = 1
				)

			order_id = Order.objects.get(user_id    = user.id).id
			carts    = Cart.objects.filter(order_id = order_id)

			if carts.filter(product_id=product_id).exists():
				cart_product = carts.get(product_id=product_id)
				cart_product.quantity = cart_product.quantity + 1
				cart_product.amount = cart_product.amount + product.price
				cart_product.save()
			else:
				Cart(
					user_id = user.id,
					order_id = order_id,
					product_id = data['product_id'],
					amount = product.price,
				).save()

			return HttpResponse(status=200)

		return HttpResponse(status=400)

	@sign_in_auth
	def get(self, request):
		user           = request.user
		carts          = Cart.objects.filter(user_id = user.id)
		data_attribute = [
			{
				'id': cart.id,
				'quantity': cart.quantity,
				'product_id':cart.product.id,
				'name': cart.product.name,
				'type': cart.product.subscribe,
				'image': cart.product.image_url,
				'price': cart.amount
			} for cart in carts
		]

		subscribe_total_price = [
			carts.filter(product__subscribe=True).aggregate(Sum('amount'))
		]
		disposable_total_price = [
			carts.filter(product__subscribe=False).aggregate(Sum('amount'))
		]
		total_price = [carts.aggregate(Sum('amount'))]

		return JsonResponse({
            'products'               : data_attribute,
            'subscribe_total_price'  : subscribe_total_price,
            'disposable_total_price' : disposable_total_price,
            'total_price'            : total_price
        }, status=200)
			
class RemoveProducts(View):
	@sign_in_auth
	def post(self, request):
        product_ids = json.loads(request.body)['product_ids']

        Cart.objects.filter(
            user_id        = request.user.id,
            product_id__in = product_ids
        ).delete()

		return HttpResponse(status=200)
