from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=150)
    terms = models.BooleanField(default=1)
    invitation_code = models.CharField(max_length=15)
    point = models.IntegerField(default=0)
    postal_code = models.CharField(max_length=20)
    road_address = models.CharField(max_length=100)
    detaile_address = models.CharField(max_length=100)
    discount = models.IntegerField(default=1)
    mobile_agreement = models.BooleanField(default=0)
    account_product = models.ManyToManyField('product.Product', through='Prescription')
    account_deliverystatus = models.ManyToManyField('order.DeliveryStatus', through='order.Order')

    class Meta:
        db_table = 'accounts'

class Recommender(models.Model):
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'recommenders'

class Prescription(models.Model):
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'prescriptions'

class PointProducts(models.Model):
    name = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    hashtag = models.CharField(max_length=45)
    image_url = models.URLField(max_length=2000)
    detail = models.TextField()
    brand = models.CharField(max_length=100)

    class Meta:
        db_table = 'point_products'

class PointImageList(models.Model):
    point_product = models.ForeignKey('PointProducts', on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'point_image_lists'

class Authentication(models.Model):
    mobile_number = models.CharField(max_length=30)
    auth_number = models.CharField(max_length=30)

    class Meta:
        db_table = 'authentications'
