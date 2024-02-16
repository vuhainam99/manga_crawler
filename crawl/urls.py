from django.urls import path,include
from crawl import views




urlpatterns = [
    path('', views.crawl,name='crawl'),
]