from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from django.http import HttpResponse

from documents.models import Document
from documents.models import CustomUser

def Profile(request):	
	searchQuery = request.GET.get('search_box', '/')  #gets search string from profile page
	userSearchQuery = request.GET.get('user_search_box', '') #gets user search string from profile page

	# finds all docs that contain the search query
	docsContainingSearchQuery = []
	allMyDocs = Document.objects.filter(owner_id=request.user.id)
	for doc in allMyDocs:
		content =  doc.content
		content = content.split('/')
		for word in content:
			if searchQuery in word:
				docsContainingSearchQuery.append(doc.id)
				break

	# finds users who's username and/or interests match user search query
	userMatches = []
	if userSearchQuery != "":
		allOUs = CustomUser.objects.filter(is_OU=True)
		for user in allOUs:
			username = user.username
			interests = user.interests
			if userSearchQuery in username:
				userMatches.append({
					'username': username,
					'interests': interests,
				})
			elif userSearchQuery in interests:
				userMatches.append({
					'username': username,
					'interests': interests,
				})

	if request.user.is_authenticated:
		my_id = str(request.user.id)
		user = CustomUser.objects.filter(id=request.user.id)
		for u in user:
			interests = u.interests
		allDocs = Document.objects.all()
		sharedDocs = []
		publicDocs = []
		for doc in allDocs:
			collaborators = doc.collaborators.split('/')
			if my_id in collaborators:
				sharedDocs.append(doc)
			if doc.private == False:
				publicDocs.append(doc)
		return render(request, 'profile.html', {
	    	'myDocs': Document.objects.filter(owner=request.user.id),
	    	'sharedDocs': sharedDocs,
	    	'publicDocs': publicDocs,
	    	'interests': interests,
	    	'docsContainingSearchQuery': docsContainingSearchQuery,
	    	'userMatches': userMatches,
	    })
	else:
		my_id = str(request.user.id)
		allDocs = Document.objects.all()
		sharedDocs = []
		publicDocs = []
		for doc in allDocs:
			collaborators = doc.collaborators.split('/')
			if my_id in collaborators:
				sharedDocs.append(doc)
			if doc.private == False:
				publicDocs.append(doc)
		return render(request, 'profile.html', {
	    	'myDocs': Document.objects.filter(owner=request.user.id),
	    	'sharedDocs': sharedDocs,
	    	'publicDocs': publicDocs,
	    	'docsContainingSearchQuery': docsContainingSearchQuery,
	    	'userMatches': userMatches,
	    })

def Home(request):
	return render(request, 'home.html')