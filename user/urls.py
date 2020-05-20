from django.urls import path

from .views import PointProductList, PointProductDetail,SignInView, SignUpView,SmsSendView,VerificationView,MyPageView

urlpatterns = [
	path('/gift', PointProductList.as_view()),
	path('/gift/<int:product_id>', PointProductDetail.as_view()),
	path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/sms', SmsSendView.as_view()),
    path('/sms/verification', VerificationView.as_view()),
    path('/user-profile', MyPageView.as_view()),
]
