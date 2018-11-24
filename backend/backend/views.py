from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from django.http import HttpResponse

from documents.models import Document

def Profile(request):
	#print(request.user.id)
	return render(request, 'profile.html', {
    	'myDocs': Document.objects.filter(owner=request.user.id)
    })