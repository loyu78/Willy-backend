import json, bcrypt, jwt ,re ,time,requests,random,string,redis
import hashlib
import hmac
import base64

from random import randint
from threading import Timer
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from datetime import timedelta, datetime
from django.utils import timezone 
from django.shortcuts import redirect, render

from willy.settings import SECRET_KEY, ACCESS_KEY, ACCESS_URI
from .utils import make_signature, sign_in_auth
from .models import Authentication, User,Social
from .models import PointProduct, PointImageList

# 포인트 몰 상품 리스트 api
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

# 포인트 몰 상품 디테일 api
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
			return JsonResponse({'product':point_product}, status=200)
		except KeyError:
			return JsonResponse({'message':'KeyError'}, status=400)

class SignUpView(View): 
    def post(self,request):
        data = json.loads(request.body)
        pattern1 = "\w+@\w+\.[\w+]{2,3}$"
        pattern2 = re.compile('[\w!@#$%]{5,20}')
        if data['social_type'] == "1" :
            VALI1 = {
                'email'              : lambda email              : True if len(re.findall(pattern1,email)) == 0 or len(email) == 0 or User.objects.filter(email = email).exists() else False,
                'mobile_number'      : lambda mobile_number      : True if len(re.findall('\D',mobile_number)) > 0 or User.objects.filter(mobile_number= mobile_number).exists()  else False,
                'terms'              : lambda terms              : True if terms == "0" else False, # 이용 약관 동의 여부 둘다 동의시 1 하나라도 미동의시 0
                'mobile_agreement'   : lambda mobile_agreement   : True if mobile_agreement == "0" else False, # 핸드폰 인증여부 인증시 1 미인증시 0
                'password'           : lambda password           : True if len(pattern2.match(password).group()) == 0 else False,
            }
            try:
                for column,action in VALI1.items():
                    if action(data[column]):
                        return JsonResponse({'message' : f'회원가입 실패 Failed : {column}'},status=400)
                hashed_pass = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
                User( 
                    name            = data['name'],
                    mobile_number   = data['mobile_number'],
                    email           = data['email'],
                    password        = hashed_pass.decode('utf-8'),
                    invitation_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                    mobile_agreement= data['mobile_agreement'],
                    terms           = data['terms'],
                    agreement       = data['agreement'],
                    social_login_id = data['social_type'],
                ).save()
                return JsonResponse({'message' : '회원가입 완료'},status=200)
            except:
                return JsonResponse({'message' : 'INVALID_KEYS'},status=400)
        elif data['social_type'] != "1":
            VALI2 = {
                'email'              : lambda email              : True if len(re.findall(pattern1,email)) == 0 or len(email) == 0 or User.objects.filter(email = email).exists() else False,
                'mobile_number'      : lambda mobile_number      : True if len(re.findall('\D',mobile_number)) > 0 or User.objects.filter(mobile_number= mobile_number).exists()  else False,
                'terms'              : lambda terms              : True if terms == "0"                                                                                           else False, # 이용 약관 동의 여부 둘다 동의시 1 하나라도 미동의시 0
                'mobile_agreement'   : lambda mobile_agreement   : True if mobile_agreement == "0"                                                                                else False, # 핸드폰 인증여부 인증시 1 미인증시 0
            }
            try:
                for column,action in VALI2.items():
                    if action(data[column]):
                        return JsonResponse({'message' : f'회원가입 실패 Failed : {column}'},status=400)
                User(
                    name            = data['name'],
                    mobile_number   = data['mobile_number'],
                    email           = data['email'],
                    invitation_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                    mobile_agreement= data['mobile_agreement'],
                    terms           = data['terms'],
                    agreement       = data['agreement'],
                    social_login_id = data['social_type'],
                    social_id       = data['social_id'],
                ).save()
                return JsonResponse({'message' : '회원가입 완료'},status=200)
            except:
                return JsonResponse({'message' : 'INVALID_KEYS'},status=400)
                
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        # judge = {}
        # for i in data:
        #     if len(data[i]) == 0:
        #         judge[i] = True
        # if len(judge) == 2 and 'password' in judge:
        #     return JsonResponse({"message": "패스워드를 입력 해주세요."},status=400)
        # if len(judge) == 3 :
        #     return JsonResponse({"message": "로그인 정보를 입력 해 주세요."},status=400)
        # if 'mobile_number' in judge:
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {'user_id':user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                    return JsonResponse({"token":token},status=200)
                else:
                    return JsonResponse({"message" : "패스워드가 틀립니다."}, status=400)
            return JsonResponse({'message' : "이메일이 존재하지 않습니다."}, status=401)
        except KeyError:
            return JsonResponse({'message':"INVALID_KEYS"},status=400)
        return JsonResponse({"message" : "error"}, status=400)
        # return JsonResponse({"message" : "error"}, status=400)

        # if 'email' in judge:
        #     try:
        #         if User.objects.filter(mobile_number = data['mobile_number']).exists():
        #             user = User.objects.get(mobile_number = data['mobile_number'])
        #             if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        #                 token = jwt.encode(
        #                     {'user_id':user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')
        #                 return JsonResponse({"token":token},status=200)
        #             else:
        #                 return JsonResponse({"message":"패스워드가 틀립니다."},status=400)
        #         return JsonResponse({'message' : "핸드폰이 존재하지 않습니다."}, status=401)
        #     except KeyError:
        #         return JsonResponse({'message':"INVALID_KEYS"},status=400)
        #     return JsonResponse({"message" : "error"},status=400)
        # return JsonResponse({"message": "error"},status=400)

class SmsSendView(View):
    timestamp = str(int(time.time() * 1000))
    def send_sms(self, mobile_number, auth_number):
        headers = {
            'Content-Type'            : "application/json; charset=UTF-8",
            'x-ncp-apigw-timestamp'   : self.timestamp,
            'x-ncp-iam-access-key'    : ACCESS_KEY,
            'x-ncp-apigw-signature-v2': make_signature(self.timestamp)
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
        
    def post(self, request):
        data = json.loads(request.body)
        try:
            input_mobile_num        = data['mobile_number']
            auth_num                = randint(10000,100000)
            auth_mobile             = Authentication.objects.get(mobile_number = input_mobile_num)
            auth_mobile.auth_number = auth_num
            auth_mobile.save()
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
        try:
            data = User.objects.filter(id = request.user.id).values('email','mobile_number','name','agreement','invitation_code','discount')
            return JsonResponse({"user_profile" : list(data)},status=200)
        except KeyError:
            return JsonResponse({"message" : "유저 정보가 일치하지 않습니다."},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "유저 정보가 존재하지 않습니다."},status=401)
            
class KakaoLoginView(View):
    def get(self,request):
        access_token = request.headers.get('Authorization',None)
        url          = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization'  :  f"Bearer {access_token}",
            'Content-type'   : 'application/x-www-form-urlencoded; charset=utf-8'
        }
        kakao_response = requests.get(url, headers = headers)
        kakao_response = json.loads(kakao_response.text)
        kakao = Social.objects.get(social_type='kakao')
        if User.objects.filter(social_login_id=kakao, social_id= kakao_response['id']).exists():
            user      = User.objects.get(social_id=kakao_response['id'])
            token     = jwt.encode({'id' : user.id},SECRET_KEY,algorithm='HS256').decode('utf-8')
            return JsonResponse({"message" : "로그인 성공","token" : token},status=200)
        else:
            return JsonResponse({"message" : "회원가입 필요","info" : kakao_response},status=200)
 
class KakaoPayView(View):
    def post(self,request):
        data = json.loads(request.body)
        me = 'http://localhost:8000'
        request_url = "https://kapi.kakao.com/v1/payment/ready"
        headers1 = {
            'Authorization' : "KakaoAK " + "adb7eb79eb94d1702a3c84bff005e31c",
            "Content-type"  : 'application/application/x-www-form-urlencoded;charset=utf-8',
        }
        params1 = {
            'cid' : "TC0ONETIME",
            'partner_order_id': '1001',
            'partner_user_id': 'willy',
            'item_name': data['product'],
            'quantity': data['quantity'],
            'total_amount': data['amount'],
            'tax_free_amount': 0,
            'vat_amount' : str(int(int(data['amount']) * 0.1)),
            'approval_url': me + '/kakaopay/purchase',
            'fail_url': me,
            'cancel_url': me,
        }
        response = requests.post(request_url,params=params1,headers=headers1)
        response = json.loads(response.text)
        return JsonResponse({"tid" : response['tid'],"next_redirect_pc_url":response['next_redirect_pc_url']},status=200)
