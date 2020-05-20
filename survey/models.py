from django.db import models

class SurveyType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'survey_types'

class SurveyQuestion(models.Model):
    survey_type = models.ForeignKey('SurveyType', on_delete=models.SET_NULL, null=True)
    question = models.CharField(max_length=200)
    sub_question = models.CharField(max_length=200)
    image_url = models.URLField(max_length=2000, null=True)
    limit = models.CharField(max_length=30, null=True)
    surveyquetion_surveyanswer = models.ManyToManyField('Surveyanswer', through='NextQuestion')

    class Meta:
        db_table = 'survey_questions'

class SurveyAnswer(models.Model):
    survey_question = models.ForeignKey('SurveyQuestion', on_delete=models.SET_NULL, null=True)
    answer = models.CharField(max_length=200)

    class Meta:
        db_table = 'survey_answers'

class NextQuestion(models.Model):
    survey_answer = models.ForeignKey('SurveyAnswer', on_delete=models.SET_NULL, null=True)
    survey_question = models.ForeignKey('SurveyQuestion', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'next_questions'

class SuitablePill(models.Model):
    survey_answer = models.ForeignKey('SurveyAnswer', on_delete=models.SET_NULL, null=True)
    recommended_product = models.ForeignKey('RecommendedProduct', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'suitable_pills'

class SurveyComent(models.Model):
    survey_answer = models.ForeignKey('SurveyAnswer', on_delete=models.SET_NULL, null=True)
    coment = models.CharField(max_length=200)

    class Meta:
        db_table = 'survey_coment'

class CustomerInformation(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    email = models.EmailField(max_length=50)
    customerinformation_recommendedproduct = models.ManyToManyField('RecommendedProduct', through='SurveyResult')

    class Meta:
        db_table = 'customer_informations'

class CustomerAnswer(models.Model):
    customer_information = models.ForeignKey('CustomerInformation', on_delete=models.SET_NULL, null=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=2000)

    class Meta:
        db_table = 'customer_answers'

class RecommendedProduct(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(max_length=2000)
    image_title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content = models.TextField()
    highlight = models.CharField(max_length=500)
    recommendedproduct_surveyanswer = models.ManyToManyField('SurveyAnswer', through='SuitablePill')

    class Meta:
        db_table = 'recommended_products'

class ImageDescription(models.Model):
    recommended_product = models.ForeignKey('RecommendedProduct', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=300)

    class Meta:
        db_table = 'image_descriptions'

class SurveyResult(models.Model):
    result_list = models.ForeignKey('ResultList', on_delete=models.SET_NULL, null=True)
    customer_information = models.ForeignKey('CustomerInformation', on_delete=models.SET_NULL, null=True)
    recommended_product = models.ForeignKey('RecommendedProduct', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'survey_results'

class ResultList(models.Model):
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=30)

    class Meta:
        db_table = 'result_lists'

class ProductContent(models.Model):
    recommended_product = models.ForeignKey('RecommendedProduct', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)
    highlight = models.CharField(max_length=500)
    link = models.TextField()

    class Meta:
        db_table = 'product_contents'
