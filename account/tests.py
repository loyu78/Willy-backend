from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from .models import PointProduct, PointImageList

class PointMallTest(TestCase):
	maxDiff = None

	def setUp(self):
		PointProduct.objects.create(
			id = 1,
			brand = "필리",
			hashtag = "#휴대용 #살균99% #프로럴향",
			name = "오삭 핸드겔",
			price = "4,500 P",
			image_url = "https://img.pilly.kr/gift/pilly/osakgel/thumbnail.jpg"
		)

		PointProduct.objects.create(
			id = 2,
			brand = "에잇샐러드",
			hashtag = "#신선함 #셰프샐러드 #당일조리",
			name = "에잇샐러드 5,000원 쿠폰",
			price = "5,000 P",
			image_url = "https://img.pilly.kr/gift/8salade/G5000/thumbnail.png"
		)

		PointProduct.objects.create(
			id = 3,
			brand = "pilly",
			hashtag = "#필리 #일요일엔소분해요",
			name = "필리 매일 챙기는 소분통",
			price = "2,000 P",
			image_url = "https://img.pilly.kr/product/tablet/v2/pillcase.png",
			detail =  "▶이용안내\n- 포인트 교환을 하면, 다음 정기배송에 같이 배송합니다.\n- 정기구독 고객만 포인트 교환이 가능합니다.\n- 필리 매일 챙기는 소분통에 인쇄된 문구는 랜덤 발송합니다.\n- 포인트 교환 후 취소는 불가합니다."
		)

		PointImageList.objects.create(
			id = 6,
			point_product = PointProduct.objects.get(id=3),
			image_url = "https://img.pilly.kr/product/detail/pillcase/point-01.jpg"
		)
		
		PointImageList.objects.create(
			id = 7,
			point_product = PointProduct.objects.get(id=3),
			image_url = "https://img.pilly.kr/product/detail/pillcase/point-02.jpg"
		)
	
	def tearDown(self):
		PointProduct.objects.all().delete()
		PointImageList.objects.all().delete()

	def test_product_list_get_success(self):
		client = Client()
		response = client.get('/my/gift')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
        		"point_products": [
					{
						"id": 1,
						"brand": "필리",
						"hashtag": "#휴대용 #살균99% #프로럴향",
						"name": "오삭 핸드겔",
						"point": "4,500 P",
						"image_url":'https://img.pilly.kr/gift/pilly/osakgel/thumbnail.jpg'
					},
					{
						"id": 2,
						"brand": "에잇샐러드",
						"hashtag": "#신선함 #셰프샐러드 #당일조리",
						"name": "에잇샐러드 5,000원 쿠폰",
						"point": "5,000 P",
						"image_url": "https://img.pilly.kr/gift/8salade/G5000/thumbnail.png"
					},
					{	
						'id': 3,
						'brand': 'pilly', 
						'hashtag': '#필리 #일요일엔소분해요',
						'name': '필리 매일 챙기는 소분통',
						'point': '2,000 P',
						'image_url': 'https://img.pilly.kr/product/tablet/v2/pillcase.png'
					}
				]
			}	
		)

	def test_product_detail_get_success(self):
		client = Client()
		response = client.get('/my/gift/3')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"detail": {
					"id": 3,
					"brand": "pilly",
					"hashtag": "#필리 #일요일엔소분해요",
					"name": "필리 매일 챙기는 소분통",
					"point": "2,000 P",
					"image_url": "https://img.pilly.kr/product/tablet/v2/pillcase.png",
					"description": "▶이용안내\n- 포인트 교환을 하면, 다음 정기배송에 같이 배송합니다.\n- 정기구독 고객만 포인트 교환이 가능합니다.\n- 필리 매일 챙기는 소분통에 인쇄된 문구는 랜덤 발송합니다.\n- 포인트 교환 후 취소는 불가합니다.",
					"images": [
						"https://img.pilly.kr/product/detail/pillcase/point-01.jpg",
						"https://img.pilly.kr/product/detail/pillcase/point-02.jpg"
					]
				}
			}
		)

