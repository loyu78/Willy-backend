from django.db import models

class Order(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.SET_NULL, null=True)
    delvery_status = models.ForeignKey('DeliveryStatus', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    recipient_name = models.CharField(max_length=50)
    recipient_mobile = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)
    road_address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100)
    messege = models.TextField()
    point = models.IntegerField(default=0)
    order_number = models.CharField(max_length=50)
    created_at = models.DateTimeField
    password = models.CharField(max_length=150)
    identification = models.BooleanField(default=1)
    shopping_charge = models.IntegerField(default=0)
    subscription = models.BooleanField(default=0)
    order_product = models.ManyToManyField('product.Product', through='Cart')

    class Meta:
        db_table = 'orders'

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
    count = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    survey_discount = models.IntegerField(default=0)
    invitation_discount = models.IntegerField(default=0)
    status = models.BooleanField(default=1)

    class Meta:
        db_table = 'carts'