from django.urls import path,include
from report import views




urlpatterns = [
    path('', views.report,name='report'),
]