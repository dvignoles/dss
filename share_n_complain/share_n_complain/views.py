from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from django.http import HttpResponse

from documents.models import Document
from documents.models import CustomUser

def Profile(request):	
	searchQuery = request.GET.get('search_box', '/')  #gets search string from profile page
	if searchQuery:
		searchQuery = searchQuery.lower()

	userSearchQuery = request.GET.get('user_search_box', '') #gets user search string from profile page
	if userSearchQuery:
		userSearchQuery = userSearchQuery.lower()

	# finds all docs that contain the search query
	docsContainingSearchQuery = []
	allMyDocs = Document.objects.filter(owner_id=request.user.id)
	for doc in allMyDocs:
		content =  doc.content
		content = content.split('/')
		content = [line.lower() for line in content]
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
					'username': username.lower(),
					'interests': interests.lower(),
				})
			elif userSearchQuery in interests:
				userMatches.append({
					'username': username.lower(),
					'interests': interests.lower(),
				})

	if request.user.is_authenticated:

		sharedDocID = request.GET.get("shared_doc_select")
		share_decision = request.GET.get("decision")

		if share_decision == 'a':
			current_doc = Document.objects.filter(id=sharedDocID)
			for doc in current_doc:
				collaborators = doc.collaborators
			current_doc.update(collaborators=(collaborators + '/'+ str(request.user.id)))
			user_id = CustomUser.objects.filter(id=request.user.id)
			print(user_id)
			for u in user_id:
				sr = u.share_requests
			sr = sr.split('/')
			shareRequests_updated = ""
			for doc_id in sr:
				if (doc_id != sharedDocID):
					shareRequests_updated = shareRequests_updated + str(doc_id) + '/'
			shareRequests_updated = shareRequests_updated[:-1]
			user_id.update(share_requests=shareRequests_updated)
			print(shareRequests_updated)
		else:
			user_id = CustomUser.objects.filter(id=request.user.id)
			for u in user_id:
				sr = u.share_requests
			sr = sr.split('/')
			shareRequests_updated = ""
			for doc_id in sr:
				if (doc_id != sharedDocID):
					shareRequests_updated = shareRequests_updated + str(doc_id) + '/'
			shareRequests_updated = shareRequests_updated[:-1]
			user_id.update(share_requests=shareRequests_updated)
			print(shareRequests_updated)

		
		my_id = str(request.user.id)
		user = CustomUser.objects.filter(id=request.user.id)
		for u in user:
			interests = u.interests
			shareRequests = u.share_requests
		allDocs = Document.objects.all()
		sharedDocs = []
		publicDocs = []
		shareRequests = shareRequests.split('/')
		sharedDocTitles = {}
		for doc in allDocs:
			collaborators = doc.collaborators.split('/')
			if my_id in collaborators:
				sharedDocs.append(doc)
			if doc.private == False:
				publicDocs.append(doc)
			if str(doc.id) in shareRequests:
				sharedDocTitles[doc.id] = doc.title			
		
		return render(request, 'profile.html', {
	    	'myDocs': Document.objects.filter(owner=request.user.id),
	    	'sharedDocs': sharedDocs,
	    	'publicDocs': publicDocs,
	    	'interests': interests,
			'sharedDocTitles': sharedDocTitles,
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