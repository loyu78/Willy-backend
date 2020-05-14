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
    image_url = models.URLField(max_length=2000)
    sub_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    heder_image_url = models.URLField(max_length=2000)
    heder_description = models.CharField(max_length=500)
    day = models.CharField(max_length=30)
    pill_image_url = models.URLField(max_length=2000)
    pill_description = models.CharField(max_length=100)
    pill_sub_description = models.CharField(max_length=100)
    pill_sub_image_url = models.URLField(max_length=2000)
    ingredient = models.TextField()
    manual_url = models.URLField(max_length=2000)
    product_category = models.ManyToManyField('Category', through='ProductCategory')
    product_account = models.ManyToManyField('account.Account', through='Subscription')
    product_review = models.ManyToManyField('Review', through='ProductReview')

    class Meta:
        db_table = 'products'

class ProductExplanation(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=200)

    class Meta:
        db_table = 'product_explanations'

class Subscription(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.SET_NULL, null=True)
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
    image_url = models.URLField(max_length=2000)
    subscription = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    content = models.TextField()

    class Meta:
        db_table = 'reviews'

class Section(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    bottle = models.TextField()
    title = models.TextField()
    effects = models.TextField()
    point = models.TextField()
    video_url = models.URLField(max_length=2000)

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
