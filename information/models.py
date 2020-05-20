from django.db import models

class PillyNews(models.Model):
    news_type = models.ForeignKey('NewsType', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.CharField(max_length=50)

    class Meta:
        db_table = 'pilly_news'

class NewsType(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'news_types'

class Question(models.Model):
    question_type = models.ForeignKey('QuestionType', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.CharField(max_length=50)

    class Meta:
        db_table = 'questions'

class QuestionType(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'question_types'

class Notice(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    class Meta:
        db_table = 'notices'

class PillyStory(models.Model):
    image_url = models.URLField(max_length=2000)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'pilly_stories'

class StoryInformation(models.Model):
    pilly_story = models.ForeignKey('PillyStory', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    image_url = models.URLField(max_length=2000)
    content = models.CharField(max_length=300)
    description = models.TextField()

    class Meta:
        db_table = 'story_informations'

class Home(models.Model):
    image_url = models.URLField(max_length=2000)
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        db_table = 'homes'

class ProductHeader(models.Model):
    image_url = models.URLField(max_length=2000)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    class Meta:
        db_table = 'product_headers'
