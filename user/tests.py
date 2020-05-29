import jwt, json, bcrypt, re, requests, random, time
from random import randint
from datetime import timedelta, datetime
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client

from willy.settings import SECRET_KEY, ACCESS_KEY, ACCESS_URI
from .models  import User, Authentication, PointProduct, PointImageList
from .utils  import make_signature, sign_in_auth, encryption

client = Client()
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
			id = 1,
			point_product_id = PointProduct.objects.get(id=3).id,
			image_url = "https://img.pilly.kr/product/detail/pillcase/point-01.jpg"
		)
		
		PointImageList.objects.create(
			id = 2,
			point_product_id = PointProduct.objects.get(id=3).id,
			image_url = "https://img.pilly.kr/product/detail/pillcase/point-02.jpg"
		)
	
	def tearDown(self):
		PointProduct.objects.all().delete()
		PointImageList.objects.all().delete()

	def test_product_list_get_success(self):
		client = Client()
		response = client.get('/user/gift')
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
		response = client.get('/user/gift/3')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(),
			{
				"detail": [
					{
						"id": 3,
						"brand": "pilly",
						"hashtag": "#필리 #일요일엔소분해요",
						"name": "필리 매일 챙기는 소분통",
						"point": "2,000 P",
						"image_url": "https://img.pilly.kr/product/tablet/v2/pillcase.png",
						"description": "▶이용안내\n- 포인트 교환을 하면, 다음 정기배송에 같이 배송합니다.\n- 정기구독 고객만 포인트 교환이 가능합니다.\n- 필리 매일 챙기는 소분통에 인쇄된 문구는 랜덤 발송합니다.\n- 포인트 교환 후 취소는 불가합니다.",
						"images": [
							{
								"0": "https://img.pilly.kr/product/detail/pillcase/point-01.jpg"
							},
							{
								"1": "https://img.pilly.kr/product/detail/pillcase/point-02.jpg"
							}
						]
					}
				]
			}
		)

class SignUpTest(TestCase):
    def test_sign_up_post_success(self):
        user = {
            "name"             : "연습연습",
            "mobile_number"    : "01045723872",
            "email"            : "ckwlghks6622@gmail.com",
            "password"         : encryption('lklaksdn3245'),
            "mobile_agreement" : "1",
            "terms"            : "1",
            "agreement"        : "0"
        }
        response = client.post('/user/sign-up', json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            email = 'seokho22@gmail.com',
            mobile_number = '01033334444',
            password = encryption('1234567')
        )

    def tearDown(self):
        User.objects.all().delete()
    
    def test_sign_in_post_success(self):
        user = {
            "email"         : "",
            "mobile_number" : "01033334444",
            "password" : "1234567"
        }
        response = client.post('/user/sign-in', json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'token' : response.json()['token']})
        
    def test_sign_in_post_key_error(self):
        user = {
            "email"         : "",
            "mobie_number" : "01033334444",
            "password" : "1234567"
        }
        response = client.post('/user/sign-in', json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {'message' : "INVALID_KEYS"})
        
class SmsSendTest(TestCase):
    timestamp = str(int(time.time() * 1000))
    def test_sms_post_success(self):
        phone = {
            "mobile_number" : "01012345678"
        }
        response = client.post('/user/sms', json.dumps(phone),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'message' : '인증 번호 발송'})
        
class VerificationTest(TestCase):
    def setUp(self):
        Authentication.objects.create(
            mobile_number = "01012345678",
            auth_number = "12345"
        )
    
    def tearDown(self):
        Authentication.objects.all().delete()
    
    def test_sms_post_success(self):
        phone = {
            "mobile_number" : "01012345678",
            "auth_number"   : Authentication.objects.get(mobile_number="01012345678").auth_number
        }
        response = client.post('/user/sms/verification', json.dumps(phone),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'message' : '인증 완료'})
