from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from django.http import HttpResponse

from documents.models import Document
from documents.models import CustomUser

def Profile(request):
	#print(request.user.id)
	user = CustomUser.objects.filter(id=request.user.id)
	for u in user:
		interests = u.interests
	print(interests)
	return render(request, 'profile.html', {
    	'myDocs': Document.objects.filter(owner=request.user.id),
    	'interests': interests,
    })