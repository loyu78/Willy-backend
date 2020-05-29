from django.urls import path

from .views import(
        HomeView,
        StoryView,
        NoticeView,
        NewsListView,
        NewsDetailView,
        FAQListView,
        DetailStoryView,
)

urlpatterns = [
        path('/home', HomeView.as_view()),
	path('', NoticeView.as_view()),
	path('/news', NewsListView.as_view()),
	path('/news/<int:news_id>', NewsDetailView.as_view()),
	path('/faq', FAQListView.as_view()),
        path('/story', StoryView.as_view()),
        path('/story/<int:story_id>', DetailStoryView.as_view()),
]
