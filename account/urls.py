from django.urls import include, path
from .views import SignInView, SignUpView,SmsSendView,VerificationView


urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/sms', SmsSendView.as_view()),
    path('/sms/verification', VerificationView.as_view()),
]