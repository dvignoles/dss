from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('create/', views.CreateDoc, name='create'),
    url(r'^addLine/(?P<doc_id>[0-9]*)$', views.AddLine, name='addLine'),
    url(r'^deleteLine/(?P<doc_id>[0-9]*)$', views.DeleteLine, name='deleteLine'),
    url(r'^updateLine/(?P<doc_id>[0-9]*)$', views.UpdateLine, name='updateLine'),
    #path('view/', views.ViewDoc, name='view'),
    url(r'^view/(?P<title>[\w\W]*)(?P<doc_id>[0-9]+)(?P<content>[\s\S]*)$', views.ViewDoc, name='view'),
]