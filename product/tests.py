from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from .models import Category, Product, Review, ProductExplanation, ProductReview
from user.models import User

class ReviewTest(TestCase):
	maxDiff = None

	def setUp(self):
		Category.objects.create(
			id=1,
			name='category',
			image_url='https://img.pilly.kr/product/v20200103/common/calmgd.png',
		)

		Product.objects.create(
			id=1,
			name='밀크씨슬',
			image_url='https://img.pilly.kr/product/v20200103/common/milkthistle.png',
			sub_name='건강한 간을 위한',
			header_image_url = 'https://img.pilly.kr/product/v20200103/milkthistle/cover-mb@3x.jpg?v=v202005191609',
			header_description = '필리 밀크씨슬은 유럽산 밀크씨슬을 이용하고 동의보감에도 소개된 울금추출분말을 포함하여 우수한 품질관리를 통해 만들었습니다.',
			day = '30일분',
			price = 11300,
			color = '#f9d4bf'
		)

		Review.objects.create(
			id=1,
			name='희**',
			product_list='(밀크씨슬)',
			subscription = '정기구독 1개월',
			image_url = 'https://img.pilly.kr/review/202005/20200512/3a28e914-b119-404c-b295-a076ebb98b66.jpeg?d=800x800',
			created_at = '2020.05.12',
			content='저번달에는'
		)

		ProductReview.objects.create(
			id=1,
			product_id=1,
			review_id=1
		)

		ProductExplanation.objects.create(
			id=1,
			product_id = Product.objects.get(id=1).id,
			content = '간 건강에 도움을 줄 수 있음',
			sub_content = '동의보감에 소개된 울금추출물 포함',
			product_content = '유럽산 밀크씨슬 260mg'
		)

	def tertDown(self):
		Review.objects.all().delete()
		Product.objects.all().delete()
		Category.objects.all().delete()
		ProductExplanation.objects.all().delete()

	def test_get_review_detail(self):
		client = Client()
		response = client.get('/product/review/1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"reviews": [
					{
						"id": 1,
						"name": "희**",
						"products": "(밀크씨슬)",
						"subscription": "정기구독 1개월",
						"image": "https://img.pilly.kr/review/202005/20200512/3a28e914-b119-404c-b295-a076ebb98b66.jpeg?d=800x800",
						"created_at": "2020.05.12",
						"content": "저번달에는"
					}
				],
				"side_products": [
					{
						"name": "밀크씨슬",
						"image": "https://img.pilly.kr/product/v20200103/common/milkthistle.png",
						"content": [
							{
								"content": "간 건강에 도움을 줄 수 있음",
								"sub_content": "동의보감에 소개된 울금추출물 포함",
								"product_content": "유럽산 밀크씨슬 260mg"
							}
						]
					}
				]
			}
		)

	def test_get_review_list(self):
		client = Client()
		response = client.get('/product/review?offset=1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"reviews": [
					{
						"id": 1,
						"name": "희**",
						"products": "(밀크씨슬)",
						"subscription": "정기구독 1개월",
						"image": "https://img.pilly.kr/review/202005/20200512/3a28e914-b119-404c-b295-a076ebb98b66.jpeg?d=800x800",
						"created_at": "2020.05.12",
						"content": "저번달에는"
					}
				]
			}
		)
