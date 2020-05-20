import sys
import os
import hashlib
import hmac
import base64
# import requests
import time
import jwt
import json
import uuid

from django.http import HttpResponse
from config import SERVICEID ,SECRET
from django.http import JsonResponse
from user.models import User

def	make_signature(timestamp):  ## 문자인증 키생성
    
  access_key = "Xvm6gmd96gX9XPdiih40"				                                            # access key id  네이버 클라우드 콘솔에서 액세스키 발급
  secret_key = "WV7BMwCLAcvZVRgfdI5lgoAvjpPmdAc2A8mI8X7h"				# secret key 네이버 클라우드 콘솔에서 액세스키 옆 시크릿 키
  secret_key = bytes(secret_key, 'UTF-8')

  uri = "/sms/v2/services/ncp:sms:kr:259148040923:pilly/messages"
  message =  "POST " + uri + "\n" + timestamp + "\n"+ access_key
  message = bytes(message, 'UTF-8')
  signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()).decode('UTF-8')
        
  return signingKey


def sign_in_auth(func): ## 로그인 데코레이터
    def wrapper_func(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        try:
            if access_token:
                data = jwt.decode(access_token, SECRET['SECRET_KEY'], algorithm='HS256')
                user            = User.objects.get(id = data['user_id'])
                request.user    = user
                return func(self, request, *args, **kwargs)

            cookie_id = request.headers.get('Cookie', uuid.uuid4())

            if User.objects.filter(anonymous=cookie_id).exists():
                user    = User.objects.get(anonymous=cookie_id)
                request.user = user
                return func(self, request, *args, **kwargs)
            user = User.objects.create(anonymous=cookie_id)
            request.user = user
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({"error_code":"INVALID_TOKEN"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"error_code":"UNKNOWN_USER"}, status = 401)
    return wrapper_func
