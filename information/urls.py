from django.urls import path

from .views import(
        HomeView, NoticeView, NewsListView, NewsDetailView, FAQListView
)

urlpatterns = [
        path('/home', HomeView.as_view()),
		path('', NoticeView.as_view()),
		path('/news', NewsListView.as_view()),
		path('/news/<int:news_id>', NewsDetailView.as_view()),
		path('/faq', FAQListView.as_view()),
]

