from django.db import models

class User(models.Model):
    is_member            = models.BooleanField(default = 1)
    name                 = models.CharField(max_length = 50, null  = True)
    mobile_number        = models.CharField(max_length = 30, null  = True)
    email                = models.EmailField(max_length= 50, unique= True, null    = True)
    password             = models.CharField(max_length = 150, null = True)
    terms                = models.BooleanField(default = 0)
    agreement            = models.BooleanField(default = 0)
    mobile_agreement     = models.BooleanField(default = 0)
    invitation_code      = models.CharField(max_length = 15, null  = True)
    point                = models.IntegerField(default = 0)
    postal_code          = models.CharField(max_length = 20, null  = True)
    road_address         = models.CharField(max_length = 100, null = True)
    detail_address       = models.CharField(max_length = 100, null = True)
    discount             = models.IntegerField(default = 1)
    user_product         = models.ManyToManyField('product.Product', through      = 'Prescription')
    user_delivery_status = models.ManyToManyField('order.DeliveryStatus', through = 'order.Order')
    social_id            = models.IntegerField(default = 0)
    social_login         = models.ForeignKey('Social', on_delete = models.SET_NULL, null = True ,default = 1)

    class Meta:
        db_table = 'users'

class Recommender(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'recommenders'

class Prescription(models.Model):
    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    product    = models.ForeignKey('product.Product', on_delete = models.SET_NULL, null = True)
    period     = models.IntegerField(default=1)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'prescriptions'

class Gift(models.Model):
    name      = models.CharField(max_length = 45)
    price     = models.DecimalFiedl(23,2)
    # one to many
    hash_tag  = models.CharField(max_length = 45)
    image_url = models.URLField(max_length  = 2000)
    detail    = models.TextField()
    brand     = models.CharField(max_length = 100)

    class Meta:
        db_table = 'gifts'

class PointImageList(models.Model):
    point_product = models.ForeignKey('PointProduct', on_delete = models.SET_NULL, null = True)
    image_url     = models.URLField(max_length                  = 2000)

    class Meta:
        db_table = 'point_image_lists'

class PhoneNumberVerfication(models.Model):
    mobile_number = models.CharField(max_length = 30)
    auth_number   = models.CharField(max_length = 30)

    class Meta:
        db_table = 'authentications'

class Social(models.Model):
    social_type = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'social_types'
