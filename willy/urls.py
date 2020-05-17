from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    #path('product', include('product.urls')),
    #path('order', include('order.urls')),
    #path('survey', include('survey.urls')),
    # path('information', include('information.urls')),
]
