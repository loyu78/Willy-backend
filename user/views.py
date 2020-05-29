import hashlib
import hmac
import base64
import json, bcrypt, jwt 
import re ,time,requests,
import random,string,redis

from random           import randint
from threading        import Timer
from django.views     import View
from django.http      import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db        import IntegrityError
from datetime         import timedelta, datetime
from django.utils     import timezone
from django.shortcuts import redirect, render

from willy.settings import SECRET_KEY, ACCESS_KEY, ACCESS_URI
from .utils         import make_signature, sign_in_auth
from .models        import Authentication, User,Social
from .models        import PointProduct, PointImageList

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
			return JsonResponse({'product':point_product}, status=200)
		except KeyError:
			return JsonResponse({'message':'KeyError'}, status=400)

class SignUpView(View): 
    EMAIL_VALIDATION_RULE    = "\w+@\w+\.[\w+]{2,3}$"
    PASSWORD_VALIDATION_RULE = re.compile('[\w!@#$%]{5,20}')
    VALIDATION_RULES         = {
        'email'           : lambda email: len(re.findall(EMAIL_VALIDATION_RULE, email)) == 0,
        'mobile_number'   : lambda mobile_number: len(re.findall('\D',mobile_number)) > 0,
        'terms'           : lambda terms: terms,
        'mobile_agreement': lambda mobile_agreement: mobile_agreement, 
        'password'        : lambda password: len(PASSWORD_VALIDATION_RULE.match(password).group()) == 0,
    }
    KAKAO_VALIDATION_RULES = VALIDATION_RULES.pop('password')

    def post(self,request):
        data       = json.loads(request.body)
        is_kakao   = data['social_type'] == 'KAKAO'
        validation = KAKAO_VALIDATION_RULES if is_kakao else VALIDATION_RULES

        try:
            for column, action in validation.items():
                if action(data[column]):
                    return JsonResponse({'message' : f'회원가입 실패 Failed : {column}'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
            User(
                name            = data['name'],
                mobile_number   = data['mobile_number'],
                email           = data['email'],
                password        = hashed_pass.decode('utf-8') if not is_kakao else None,
                invitation_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                mobile_agreement= data['mobile_agreement'],
                terms           = data['terms'],
                agreement       = data['agreement'],
                social_login_id = data['social_type'],
                social_id       = data['social_id'] if is_kakao else None
            ).save()
            return JsonResponse({'message' : '회원가입 완료'},status=200)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'},status=400)
        except User.IntegrationException:
            return JsonResponse({'message' : 'User Already Exists'},status=401)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        judge = {}
        
        for field in data:
            if len(data[field]) == 0:
                judge[i] = True
        if len(judge) == 2 and 'password' in judge:
            return JsonResponse({"message": "패스워드를 입력 해주세요."},status=400)
        if len(judge) == 3 :
            return JsonResponse({"message": "로그인 정보를 입력 해 주세요."},status=400)

        email        = data.get('email')
        phone_number = data.get('phone_number')

        if email:
            user = User....
        else:
            user = User...




        if 'mobile_number' in judge:
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

        if 'email' in judge:
            try:
                if User.objects.filter(mobile_number = data['mobile_number']).exists():
                    user = User.objects.get(mobile_number = data['mobile_number'])
                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode(
                            {'user_id':user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                        return JsonResponse({"token":token},status=200)
                    else:
                        return JsonResponse({"message":"패스워드가 틀립니다."},status=400)
                return JsonResponse({'message' : "핸드폰이 존재하지 않습니다."}, status=401)
            except KeyError:
                return JsonResponse({'message':"INVALID_KEYS"},status=400)
            return JsonResponse({"message" : "error"},status=400 )

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
        response = requests.post(ACCESS_URI, headers = headers , data = body, timeout = 3)
        
    def post(self, request):
        data             = json.loads(request.body)
        input_mobile_num = data['mobile_number']
        auth_num         = randint(10000,100000)

        Authentication.objects.create(
            mobile_number = input_mobile_num,
            auth_number   = auth_num,
        ).save()
        self.send_sms(mobile_number = input_mobile_num, auth_number = auth_num)

        return JsonResponse({'message':'인증 번호 발송'}, status=200)

class VerificationView(View):
    def post(self, request):
        data = json.loads(request.body)

        if Authentication.objects.filter(
            mobile_number = data['mobile_number'],
            auth_number   = data['auth_number']
        ).exists():
            return JsonResponse({'message': '인증 완료'},status=200)
        else:
            return JsonResponse({'message': '인증 실패'},status=401)
    
class MyPageView(View):
    @sign_in_auth
    def get(self,request):
        try:
            user = (
                User
                .objects
                .get(id = request.user.id)
                .values(
                    'email',
                    'mobile_number',
                    'name',
                    'agreement',
                    'invitation_code',
                    'discount'
                )
            )
            return JsonResponse({"user_profile" : user}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message" : "유저 정보가 존재하지 않습니다."},status=401)
            
class KakaoLoginView(View):
    def get(self,request):
        access_token = request.headers.get('Authorization')
        url          = 'https://kapi.kakao.com/v2/user/me'
        headers      = {
            'Authorization'  :  f"Bearer {access_token}",
            'Content-type'   : 'application/x-www-form-urlencoded; charset=utf-8'
        }
        kakao_response = requests.get(url, headers       = headers, timeout = 1)
        kakao_response = json.loads(kakao_response.text)
        kakao          = Social.objects.get(social_type  = 'kakao')

        if User.objects.filter(social_login_id=kakao, social_id= kakao_response['id']).exists():
            user      = User.objects.get(social_id=kakao_response['id'])
            token     = jwt.encode({'id' : user.id},SECRET_KEY,algorithm='HS256').decode('utf-8')

            return JsonResponse({"message" : "로그인 성공","token" : token},status=200)
        else:
            return JsonResponse({"message" : "회원가입 필요"}, status=401)
 
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
