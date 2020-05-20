from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'categories'

class ProductCategory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'products_categories'

class Product(models.Model):
    name = models.CharField(max_length=50)
    subscribe = models.BooleanField(default=1)
    image_url = models.URLField(max_length=2000)
    sub_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    header_image_url = models.URLField(max_length=2000)
    header_description = models.CharField(max_length=500)
    day = models.CharField(max_length=30)
    pill_image_url = models.URLField(max_length=2000, null=True)
    pill_description = models.CharField(max_length=100, null=True)
    pill_sub_description = models.CharField(max_length=100, null=True)
    pill_sub_image_url = models.URLField(max_length=2000, null=True)
    ingredient = models.TextField(null=True)
    manual_url = models.URLField(max_length=2000, null=True)
    color = models.CharField(max_length=50)
    product_category = models.ManyToManyField('Category', through='ProductCategory')
    product_user = models.ManyToManyField('user.User', through='Subscription')
    product_review = models.ManyToManyField('Review', through='ProductReview')

    class Meta:
        db_table = 'products'

class ProductExplanation(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=200)
    sub_content = models.CharField(max_length=200)
    product_content = models.CharField(max_length=200)

    class Meta:
        db_table = 'product_explanations'

class Subscription(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'subscriptions'

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    review = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'products_reviews'

class Review(models.Model):
    name = models.CharField(max_length=100)
    product_list = models.CharField(max_length=200)
    image_url = models.URLField(max_length=2000)
    subscription = models.CharField(max_length=100)
    created_at = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = 'reviews'

class Section(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    bottle = models.TextField()
    title = models.TextField(null=True)
    effects = models.TextField(null=True)
    point = models.TextField(null=True)
    video_url = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'sections'

class FrequentQuestion(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'frequent_questions'

class Material(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    nutrial = models.CharField(max_length=50)
    image_url = models.URLField(max_length=2000)
    precautions = models.TextField()

    class Meta:
        db_table = 'materials'

class Explanation(models.Model):
    image_url = models.URLField(max_length=2000)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)

    class Meta:
        db_table = 'explanations'
