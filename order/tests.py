import json
import bcrypt
import jwt

from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from config import token
from .models import Order, Cart, OrderStatus
from user.models import User
from product.models import Product, Category

class CartTest(TestCase):
	maxDiff = None
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		User.objects.create(
			id = 13,
			name='heejin',
			email='heejin@heejin.com',
			password='heejin',
			mobile_number='01011111111',
			terms='1',
			mobile_agreement='1',
			agreement='0'
		)
		
		Product.objects.create(
			id=1,
			name='루테인',
			image_url='https://img.pilly.kr/product/v20200103/common/lutein.png',
			sub_name='눈 건강을 위한',
			header_image_url = 'https://img.pilly.kr/product/v20200103/lutein/cover@3x.jpg?v=v202004161230',
			header_description = '필리 루테인은 인도 카르나타카에서 재배된 마리골드꽃추출물을 사용하고 어두운 곳에서 시각 적응을 위해 필요한 비타민A를 포함하여 우수한 품질관리를 통해 만들었습니다.',
			day = '30일분',
			color = '#f9d4bf',
		)
		
		OrderStatus.objects.create(
			id = 1,
			status = '주문전'
		)

		Order.objects.create(
			id = 1,
			user_id = User.objects.get(id=13).id,
			order_status_id = OrderStatus.objects.get(id=1).id
		)
		
		Cart.objects.create(
			id = 1,
			user_id=User.objects.get(id=13).id,
			order_id=Order.objects.get(id=1).id,
			product_id=1,
			amount=10600
		)

	def tearDown(self):
		Cart.objects.all().delete()
		User.objects.all().delete()
		Product.objects.all().delete()
		Category.objects.all().delete()
		Order.objects.all().delete()

	def test_post_cart(self):
		user = User.objects.get(id = 13)
		client = Client()
		cart = {
			"product_id":1
		}
		response = client.post('/order/cart', json.dumps(cart), content_type='application/json', **{'HTTP_authorization' : token['token']})
		self.assertEqual(response.status_code, 200)

	def test_get_cart(self):
		client = Client()
		header = {
			'HTTP_Authorization':token['token']
		}
		response = client.get('/order/cart', **header)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"products": [
					{
						"id": 1,
						"quantity": 1,
						"product_id": 1,
						"name": "루테인",
						"type": True,
						"image": "https://img.pilly.kr/product/v20200103/common/lutein.png",
						"price": 10600
					}
				],
				"subscribe_total_price": [
					{
						"amount__sum": 10600
					}
				],
				"disposable_total_price": [
					{
						"amount__sum": None
					}
				],
				"total_price": [
					{
						"amount__sum": 10600
					}
				]
			}
		)

	def test_get_remove_products(self):
		client = Client()
		header = {
			'HTTP_Authorization':token['token']
		}
		response = client.get('/order/cart/remove', **header)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"message": "remove success"
			}
		)

	def test_get_remove_product_susscess(self):
		client = Client()
		header = {
			'HTTP_Authorization':token['token']
		}
		response = client.get('/order/cart/remove/1', **header)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"message": "remove success"
			}
		)

	def test_get_remove_product_fail(self):
		client = Client()
		header = {
			'HTTP_Authorization':token['token']
		}
		response = client.get('/order/cart/remove/5', **header)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(),
			{
				"message": "invalid"
			}
		)	
