import json

from django.views import View
from django.http  import HttpResponse, JsonResponse

from .models import (
    Home,
    Notice,
    PillyNews,
    Question,
    ProductHeader,
    PillyStory,
    StoryInformation
)

class HomeView(View):
    def get(self, request):
        home_list = Home.objects.all().values()

        return JsonResponse({'home_list':list(home_list)}, status=200)

class NoticeView(View):
	def get(self, request):
		terms   = request.GET.get('terms', '이용약관')
		notices = Notice.objects.filter(title = terms).values()

		return JsonResponse({'terms':list(notices)}, status=200)

class NewsListView(View):
	def get(self, request):
        limit  = request.GET['limit', 20]
        offset = request.GET['offset', 0]

        news_list = PillyNews.objects.all()[limit:offset]
		data      = [
			{
				'id'         : news.id,
				'type'       : news.news_type.name,
				'title'      : news.title,
				'created_at' : news.created_at
			} for news in news_list
		]
		return JsonResponse({'news_list':data}, status=200)

class NewsDetailView(View):
	def get(self, request, news_id):
		news = PillyNews.objects.get(id=news_id)
		data = [
			{
				'id'         : news.id,
				'type'       : news.news_type.name,
				'title'      : news.title,
				'content'    : news.content,
				'created_at' : news.created_at
			}
		]
		return JsonResponse({'news':data}, status=200)

class FAQListView(View):
	def get(self, request):
        limit  = request.GET['limit', 20]
        offset = request.GET['offset', 0]

        questions = Question.objects.all()[limit:offset]
		data      = [
			{
				'id'         : question.id,
				'type'       : question.question_type.name,
				'title'      : question.title,
				'content'    : question.content,
				'created_at' : question.created_at
			} for question in questions
		]
		return JsonResponse({'faq_list':data}, status=200)

class StoryView(View):
    def get(self, request):
        limit    = request.GET['limit', 20]
        offset   = request.GET['offset', 0]
        category = request.GET.get('category', None)

        if category:
            stories = StoryInformation.objects.filter(pilly_story__name=category)[limit:offset]
        else:
            stories = StoryInformation.objects.all()[limit:offset]

        stories = [
            story.values(
                'id',
                'image_url',
                'pilly_story__name',
                'title',
                'content'
            ) for story in stories
        ]

        return JsonResponse({'stories' : story_list}, status=200)

class DetailStoryView(View):
    def get(self, request, story_id):
        detail = StoryInformation.objects.filter(id=story_id).values()
        return JsonResponse({'detail':list(detail)})
