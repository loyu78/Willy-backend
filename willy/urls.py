from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('information', include('information.urls')),
    path('product', include('product.urls')),
    path('order', include('order.urls')),
]
