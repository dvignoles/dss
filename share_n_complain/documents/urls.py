#### Urls tell Django which function in the documents/views.py file to load when a specific url is accessed from the browser
#### The regular expressions on some of these urls capture the specific document id that a user is using and passes it to the 
####    corresponding view function


from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('create/', views.CreateDoc, name='create'),
    url(r'^addLine/(?P<doc_id>[0-9]*)$', views.AddLine, name='addLine'),
    url(r'^deleteLine/(?P<doc_id>[0-9]*)$', views.DeleteLine, name='deleteLine'),
    url(r'^updateLine/(?P<doc_id>[0-9]*)$', views.UpdateLine, name='updateLine'),
    url(r'^fixTaboo/(?P<doc_id>[0-9]*)$', views.FixTaboo, name='fixTaboo'),
    url(r'^shareDoc/(?P<doc_id>[0-9]*)$', views.ShareDoc, name='shareDoc'),
    url(r'^view/(?P<doc_id>[0-9]*)$', views.ViewDoc, name='view'),
    url(r'^viewOldVersion/(?P<doc_id>[0-9]*)(?P<delimiter>[|]+)(?P<oldVersion>[0-9]*)$', views.ViewOldVersion, name='viewOldVersion'),
    url(r'^changeLockedStatus/(?P<doc_id>[0-9]*)$', views.ChangeLockedStatus, name='changeLockedStatus'),
    url(r'^complain/(?P<doc_id>[0-9]*)$', views.Complain, name='complain'),
    url(r'^complaint_dismiss/(?P<comp_id>[0-9]*)$', views.Complaint_Dismiss, name = 'complaint_dismiss'),
    url(r'^complaint_remove_user/(?P<comp_id>[0-9]*)$', views.Complaint_Remove_User, name = 'complaint_remove_user'),
    url(r'^complain_owner/(?P<doc_id>[0-9]*)$', views.Complain_Owner, name='complain_owner')
 
]