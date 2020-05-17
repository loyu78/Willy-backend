from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=150)
    terms = models.BooleanField(default=0)
    agreement = models.BooleanField(default=0)
    invitation_code = models.CharField(max_length=15,unique=True)
    point = models.IntegerField(default=0)
    postal_code = models.CharField(max_length=20, null=True)
    road_address = models.CharField(max_length=100, null=True)
    detail_address = models.CharField(max_length=100, null=True)
    discount = models.IntegerField(default=0)
    mobile_agreement = models.BooleanField(default=0)
    account_product = models.ManyToManyField('product.Product', through='Prescription')
    account_deliverystatus = models.ManyToManyField('order.DeliveryStatus', through='order.Order')

    class Meta:
        db_table = 'accounts'
        
class Recommender(models.Model):
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'recommenders'

class Prescription(models.Model):
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'prescriptions'

class PointProduct(models.Model):
    name = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    hashtag = models.CharField(max_length=45)
    image_url = models.URLField(max_length=2000)
    detail = models.TextField()
    brand = models.CharField(max_length=100)

    class Meta:
        db_table = 'point_products'

class PointImageList(models.Model):
    point_product = models.ForeignKey('PointProduct', on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'point_image_lists'

class Authentication(models.Model):
    mobile_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'authentications'
        