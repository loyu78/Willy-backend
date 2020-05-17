import json, bcrypt, jwt ,re ,time,requests,random,string,redis
from random import randint
from threading import Timer
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from datetime import timedelta ,datetime
from django.utils import timezone
from willy.settings import SECRET_KEY,ACCESS_KEY,ACCESS_URI
from utils import make_signature , user_authentication
from .models import Authentication,Account

class SignUpView(View): ## 회원가입
    
    def post(self,request):
        data = json.loads(request.body)
        # print(data)
        pattern1 = "\w+@\w+\.[\w+]{2,3}$"
        pattern2 = re.compile('[\w!@#$%]{5,20}')
        
        VALI = {
            'email'              : lambda email              : True if len(re.findall(pattern1,email)) == 0 or len(email) == 0 or Account.objects.filter(email = email).exists() else False,
            'mobile_number'      : lambda mobile_number      : True if len(re.findall('\D',mobile_number)) > 0 or Account.objects.filter(mobile_number= mobile_number).exists()  else False,
            'terms'              : lambda terms              : True if terms == "0"                                                                                              else False, # 이용 약관 동의 여부 둘다 동의시 1 하나라도 미동의시 0
            'mobile_agreement'   : lambda mobile_agreement   : True if mobile_agreement == "0"                                                                                   else False, # 핸드폰 인증여부 인증시 1 미인증시 0
            'password'           : lambda password           : True if len(pattern2.match(password).group()) == 0                                                                else False,
        }
        
        try:
            for column,action in VALI.items():
                if action(data[column]):
                    return JsonResponse({'message' : '회원가입 실패'},status=400)
            hashed_pass = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
            Account(  # 포인트는 Default 0 이므로 삽입 불필요
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
                if Account.objects.filter(email = data['email']).exists():
                    user = Account.objects.get(email = data['email'])
                            
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
                if Account.objects.filter(mobile_number = data['mobile_number']).exists():
                    user = Account.objects.get(mobile_number = data['mobile_number'])
                            
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
    def send_sms(self, mobile_number, auth_number):

        headers = {
            'Content-Type'            : "application/json; charset=UTF-8",
            'x-ncp-apigw-timestamp'   : self.timestamp,
            'x-ncp-iam-access-key'    : ACCESS_KEY,
            'x-ncp-apigw-signature-v2': make_signature(self.timestamp),
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