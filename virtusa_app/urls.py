from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.front,name="front"),
path('/front/sentiment/', views.sentiment,name="sentiment"),
path('/front/lifeinsurance/', views.index,name="index"),
path('/front/lifeinsurance/Finaloutput', views.clustering,name="clustering"),
path('/front/sentiment/tweets', views.tweets,name="tweets"),
]