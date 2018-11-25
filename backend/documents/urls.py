from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('create/', views.CreateDoc, name='create'),
    #path('view/', views.ViewDoc, name='view'),
    url(r'^view/(?P<title>[\w\W]*)(?P<doc_id>[0-9]+)(?P<content>[\s\S]*)$', views.ViewDoc, name='view'),
]