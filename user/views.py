import json, bcrypt, jwt, re, time, requests, random, string, redis
import hashlib
import hmac
import base64

from django.http import JsonResponse, HttpResponse
from django.views import View

from random import randint
from threading import Timer
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from datetime import timedelta ,datetime
from django.utils import timezone
from willy.settings import SECRET_KEY,ACCESS_KEY,ACCESS_URI
from .utils import make_signature , sign_in_auth

from .models import (
	PointProduct, PointImageList,
	Authentication, User,
)


class PointProductList(View):
	def get(self, request):
		products = PointProduct.objects.values()
		point_products = [
			{
				'id':product['id'],
				'brand':product['brand'],
				'hashtag':product['hashtag'],
				'name':product['name'],
				'point':product['price'],
				'image_url':product['image_url']
			} for product in products
		]
		return JsonResponse({'point_products':point_products}, status=200)

class PointProductDetail(View):
	def get(self, request, product_id):
		try:
			product = PointProduct.objects.prefetch_related('pointimagelist_set').get(id=product_id)
			images = product.pointimagelist_set.filter(point_product_id=product_id)
			point_product = [{
				'id':product.id,
				'brand':product.brand,
				'hashtag':product.hashtag,
				'name':product.name,
				'point':product.price,
				'image_url':product.image_url,
				'description':product.detail,
				'images':[{idx:image.image_url} for idx, image in enumerate(images)]
			}]
			return JsonResponse({'detail':point_product}, status=200)
		except KeyError:
			return JsonResponse({'message':'KeyError'}, status=400)

class SignUpView(View): ## 회원가입
    
    def post(self,request):
        data = json.loads(request.body)
        # print(data)
        pattern1 = "\w+@\w+\.[\w+]{2,3}$"
        pattern2 = re.compile('[\w!@#$%]{5,20}')
        
        VALI = {
            'email'              : lambda email              : True if len(re.findall(pattern1,email)) == 0 or len(email) == 0 or User.objects.filter(email = email).exists() else False,
            'mobile_number'      : lambda mobile_number      : True if len(re.findall('\D',mobile_number)) > 0 or User.objects.filter(mobile_number= mobile_number).exists()  else False,
            'terms'              : lambda terms              : True if terms == "0"                                                                                              else False, # 이용 약관 동의 여부 둘다 동의시 1 하나라도 미동의시 0
            'mobile_agreement'   : lambda mobile_agreement   : True if mobile_agreement == "0"                                                                                   else False, # 핸드폰 인증여부 인증시 1 미인증시 0
            'password'           : lambda password           : True if len(pattern2.match(password).group()) == 0                                                                else False,
        }
        
        try:
            for column,action in VALI.items():
                if action(data[column]):
                    return JsonResponse({'message' : f'회원가입 실패 Failed : {column}'},status=400)
            hashed_pass = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
            User(  # 포인트는 Default 0 이므로 삽입 불필요
                name            = data['name'],
                mobile_number   = data['mobile_number'],
                email           = data['email'],
                password        = hashed_pass.decode('utf-8'),
                invitation_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                mobile_agreement= data['mobile_agreement'],
                terms           = data['terms'],
                agreement       = data['agreement']
            ).save()
            return JsonResponse({'message' : '회원가입 완료'},status=200)
        except:
            return JsonResponse({'message' : 'INVALID_KEYS'},status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if len(data['email']) > 0:
            try:
                if User.objects.filter(email = data['email']).exists():
                    user = User.objects.get(email = data['email'])
                            
                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        print(bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')))
                        token = jwt.encode(
                            {'user_id':user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')

                        return JsonResponse({"token":token},status=200)
                return JsonResponse({'message' : "EMAIL_DOES_NOT_EXIST"}, status=401)

            except KeyError:
                return JsonResponse({'message':"INVALID_KEYS"},status=400)
        else:
            try:
                if User.objects.filter(mobile_number = data['mobile_number']).exists():
                    user = User.objects.get(mobile_number = data['mobile_number'])
                            
                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        print(bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')))
                        token = jwt.encode(
                            {'user_id':user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')

                        return JsonResponse({"token":token},status=200)
                return JsonResponse({'message' : "MOBILE_DOES_NOT_EXIST"}, status=401)

            except KeyError:
                return JsonResponse({'message':"INVALID_KEYS"},status=400)

class SmsSendView(View):
    timestamp = str(int(time.time() * 1000))
    def	make_signature(self,timestamp):  ## 문자인증 키생성
            
        access_key = "Xvm6gmd96gX9XPdiih40"				                                            # access key id  네이버 클라우드 콘솔에서 액세스키 발급
        secret_key = "WV7BMwCLAcvZVRgfdI5lgoAvjpPmdAc2A8mI8X7h"				# secret key 네이버 클라우드 콘솔에서 액세스키 옆 시크릿 키
        secret_key = bytes(secret_key, 'UTF-8')

        uri = "/sms/v2/services/ncp:sms:kr:259148040923:pilly/messages"
        message =  "POST " + uri + "\n" + timestamp + "\n"+ access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()).decode('UTF-8')
                
        return signingKey
    def send_sms(self, mobile_number, auth_number):

        headers = {
            'Content-Type'            : "application/json; charset=UTF-8",
            'x-ncp-apigw-timestamp'   : self.timestamp,
            'x-ncp-iam-access-key'    : ACCESS_KEY,
            'x-ncp-apigw-signature-v2': self.make_signature(self.timestamp)
        }

        body = {
            "type": "SMS",
            "contentType": "COMM",
            "from": "01064253526",
            "content": f"[필리 인증번호:{auth_number}] 필리 가입을 위한 인증번호입니다. 3분 이내에 입력 후 인증하세요.",
            "messages": [{"to": f"{mobile_number}"}]
        }
        body = json.dumps(body)
        response = requests.post(ACCESS_URI, headers = headers , data = body)
        print("response.status_code=",end=""), print(response.status_code)
        
    def post(self, request):
        data = json.loads(request.body)
        # # temp = redis.StrictRedis()
        # condition = re.compile('\d{11}').match(data['mobile_number']).group()
        # print(condition)
        # print(data['mobile_number'] != condition)
        # if data['mobile_number'] != condition:
        #     return JsonResponse({'message':'핸드폰 형식이 맞지 않습니다.'},status=400)
        try:
            input_mobile_num        = data['mobile_number']
            auth_num                = randint(10000,100000)
            auth_mobile             = Authentication.objects.get(mobile_number = input_mobile_num)
            auth_mobile.auth_number = auth_num
            auth_mobile.save()
        # temp.set(data['mobile_number'],randint(10000,100000))
        # temp.expire(data['mobile_number'], 15)
        # print(temp)
            self.send_sms(mobile_number = data['mobile_number'], auth_number = auth_num)
            return JsonResponse({'message':'인증 번호 발송'}, status=200)
        except Authentication.DoesNotExist:
            Authentication.objects.create(
                mobile_number = input_mobile_num,
                auth_number   = auth_num,
            ).save()
            
            self.send_sms(mobile_number = input_mobile_num, auth_number = auth_num)
            return JsonResponse({'message':'인증 번호 발송'}, status=200)

class VerificationView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            verifi = Authentication.objects.get(mobile_number=data['mobile_number'])
            if verifi.auth_number == data['auth_number']:
                return JsonResponse({'message': '인증 완료'},status=200)
            else:
                return JsonResponse({'message': '인증 실패'},status=400)
        except Authentication.DoesNotExist:
            return JsonResponse({'message' : '인증 오류'},status=400)
        
        
class MyPageView(View):
    
    @sign_in_auth
    def get(self,request):
        print("유저는",request.user)
        try:
            data = User.objects.filter(id = request.user.id).values('email','mobile_number','name','agreement','invitation_code','discount')
            
            return JsonResponse({"user_profile" : list(data)},status=200)
        
        except KeyError:
            return JsonResponse({"message" : "유저 정보가 일치하지 않습니다."},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "유저 정보가 존재하지 않습니다."},status=401)
