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

# 장바구니 api
class CartView(View):
	@sign_in_auth
	def post(self, request):
		try:
			data = json.loads(request.body)
			if 'product_id' in data:
				product_id = data['product_id']
				product = Product.objects.get(id=product_id)
				user = request.user

                # 진행중인 주문이 있으면 해당 주문 id를 가져오고, 없으면 생성
				if Order.objects.filter(user_id=user.id, order_status_id=1).exists():
					order_id = Order.objects.get(user_id=user.id).id
				else:
					Order.objects.create(
						user_id = User.objects.get(id=user.id).id,
						order_status_id = 1
					)

				order_id = Order.objects.get(user_id=user.id).id
				carts = Cart.objects.filter(order_id=order_id)
                # 장바구니에 해당 제품이 있으면 수량, 가격을 업데이트
				if carts.filter(product_id=product_id).exists():
					cart_product = carts.get(product_id=product_id)
					cart_product.quantity = cart_product.quantity + 1
					cart_product.amount = cart_product.amount + product.price
					cart_product.save()
                # 없으면 장바구니에 생성
				else:
					Cart(
						user_id = user.id,
						order_id = order_id,
						product_id = data['product_id'],
						amount = product.price,
					).save()
				return JsonResponse({'message':'success'}, status=200)
		except KeyError:
			return JsonResponse({'message':'key error'}, status=200)

    # 장바구니에 담긴 제품 보여주는 api
	@sign_in_auth
	def get(self, request):
		user = request.user
		carts = Cart.objects.filter(user_id=user.id)
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
		total_price = [
			carts.aggregate(Sum('amount'))
		]
		return JsonResponse({'products':data_attribute, 'subscribe_total_price':subscribe_total_price, 'disposable_total_price':disposable_total_price,'total_price':total_price}, status=200)
			
# 장바구니 비우기 api
class RemoveProducts(View):
	@sign_in_auth
	def delete(self, request):
		user = request.user
		carts = Cart.objects.filter(user_id=user.id)
		if carts.exists():
			carts.delete()
			return JsonResponse({'message':'remove success'}, status=200)
		return JsonResponse({'message':'invalid'}, status=400)

# 장바구니에 담긴 제품 1개씩 지우는 api
class RemoveProduct(View):
	@sign_in_auth
	def delete(self, request, product_id):
		try:
			user = request.user
			cart = Cart.objects.filter(user_id=user.id)
			if cart.exists():
				product = cart.get(product_id=product_id)
                # 수량이 1개면 완전히 지우기
				if product.quantity == 1:
					product.delete()
					return JsonResponse({'message':'remove success'}, status=200)
                # 수량이 2개 이상이면 1개만 지우고 수량, 가격 수정
				if product:
					product.quantity = product.quantity - 1
					product.amount = product.amount - product.product.price
					product.save()
					return JsonResponse({'message':'remove success'}, status=200)
			return JsonResponse({'message':'invalid'}, status=400)
		except Cart.DoesNotExist:
			return JsonResponse({'message':'invalid'}, status=400)
