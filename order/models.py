from django.db import models


class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    delvery_status = models.ForeignKey('DeliveryStatus', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True)
    mobile_number = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    recipient_name = models.CharField(max_length=50, null=True)
    recipient_mobile = models.CharField(max_length=30, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    road_address = models.CharField(max_length=100, null=True)
    detail_address = models.CharField(max_length=100, null=True)
    messege = models.TextField(null=True)
    point = models.IntegerField(default=0)
    order_number = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField
    password = models.CharField(max_length=150, null=True)
    identification = models.BooleanField(default=1)
    subscription = models.BooleanField(default=0)
    order_product = models.ManyToManyField('product.Product', through='Cart')
    status = models.BooleanField(default=0)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_status'

class DeliveryStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'delivery_status'

class Payment(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'payments'

class Cart(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    survey_discount = models.IntegerField(default=0)
    invitation_discount = models.IntegerField(default=0)

    class Meta:
        db_table = 'carts'
