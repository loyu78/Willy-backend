from django.urls import include, path
from .views import SignInView, SignUpView,SmsSendView,VerificationView,PointProductList, PointProductDetail


urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/sms', SmsSendView.as_view()),
    path('/sms/verification', VerificationView.as_view()),
  	path('/gift', PointProductList.as_view()),
	  path('/gift/<int:product_id>', PointProductDetail.as_view()),
]