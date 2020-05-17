import jwt , json,bcrypt,re,requests,random,time
from random import randint
from datetime import timedelta, datetime
from .models  import Account,Authentication
from django.test import TestCase, Client
from unittest.mock     import patch, MagicMock
from willy.settings import SECRET_KEY,ACCESS_KEY,ACCESS_URI
from utils  import make_signature,user_authentication
client = Client()


class SignUpTest(TestCase):
    
    # def setUp(self):
        
    
    def test_sign_up_post_success(self):
        
        user = {
            "name"             : "연습연습",
            "mobile_number"    : "01045723872",
            "email"            : "ckwlghks6622@gmail.com",
            "password"         : bcrypt.hashpw('abcdefg123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "mobile_agreement" : "1",
            "terms"            : "1",
            "agreement"        : "0"
        }
        
        response = client.post('/account/sign-up', json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
class SignInTest(TestCase):
    
    def setUp(self):
        Account.objects.create(
            email = 'seokho22@gmail.com',
            mobile_number = '01033334444',
            password = bcrypt.hashpw('1234567'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        Account.objects.all().delete()
    
    
    def test_sign_in_post_success(self):
        user = {
            "email"         : "",
            "mobile_number" : "01033334444",
            "password" : "1234567"
        }
        
        response = client.post('/account/sign-in', json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'token' : response.json()['token']})
        
    def test_sign_in_post_key_error(self):
        user = {
            "email"         : "",
            "mobie_number" : "01033334444",
            "password" : "1234567"
        }
        
        response = client.post('/account/sign-in', json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {'message' : "INVALID_KEYS"})
        
class SmsSendTest(TestCase):
    timestamp = str(int(time.time() * 1000))
    
    def test_sms_post_success(self):
        phone = {
            "mobile_number" : "01012345678"
        }
        response = client.post('/account/sms', json.dumps(phone),content_type='application/json')
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
        response = client.post('/account/sms/verification', json.dumps(phone),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'message' : '인증 완료'})