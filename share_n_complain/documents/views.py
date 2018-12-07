from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .forms import DocumentCreationForm, AddLineForm, DeleteLineForm, UpdateLineForm, ShareDocForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from documents.models import Document, History
from users.models import CustomUser

from users.views import getOuUsernames

# class CreateDoc(generic.CreateView):
# 	form_class = DocumentCreationForm
# 	success_url = reverse_lazy('profile')
# 	template_name = 'createDoc.html'
# 	#initial = {'owner': self.request.user.id}
# 	owner_id = HttpResponse(str(request.user.id))

# # def CreateDocForm(request):
# # 	form = CreateDoc(initial=dict(owner=request.user.id))
# # 	template_name = 'createDoc.html'
# # 	return render(request, template_name, form)

# def get_user_id(request):
# 	return request.user.id

# def CreateDoc(request):
#     form = DocumentCreationForm(request=request)
#     template_name = 'createDoc.html'
#     context = {'form': form}
#     #form.save()
#     return render(request, template_name, context)

# @login_required(login_url='sign_in')
def CreateDoc(request):
    if request.method == 'POST':
        form = DocumentCreationForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
            doc.save()
            #return HttpResponse('Your document ' + doc.title + ' was saved!')
            #return render(request, 'profile.html')
            return HttpResponseRedirect('/profile')
    else:
        form = DocumentCreationForm()
    return render(request, 'createDoc.html', {
        'form': form
    })

def ChangeLockedStatus(request, doc_id):
	docs = Document.objects.filter(id=doc_id)
	for doc in docs:
		if doc.locked:
			Document.objects.filter(id=doc_id).update(locked=0)
		else:
			Document.objects.filter(id=doc_id).update(locked=1, locked_by=request.user.id)
		return HttpResponseRedirect('/documents/view/' + doc_id)

def ViewDoc(request, doc_id):
	docs = Document.objects.filter(id=doc_id)
	docHistory = History.objects.filter(doc_id=doc_id)
	for doc in docs:
		owner_id = doc.owner_id
		title = doc.title
		content = doc.content
		private = doc.private
		collaborators = doc.collaborators
		version = doc.version
		locked = doc.locked
		locked_by = doc.locked_by
	try:
		editor = CustomUser.objects.get(id=locked_by)
	except:
		editor = 'none'
		print('Document has not been locked yet')
	collaborators = collaborators.split('/')
	if str(request.user.id) in collaborators:
		is_collaborator = True
	else:
		is_collaborator = False
	return render(request, 'viewDoc.html', {
		'user_id': str(request.user.id),
		'owner_id': str(owner_id),
		'title': title,
		'private': private,
		'doc_id': doc_id,
    	'content': content.split('/'),
    	'is_collaborator': is_collaborator,
    	'version': version,
    	'docHistory': docHistory,
    	'locked': locked,
    	'locked_by': str(locked_by),
    	'editor': editor,
    })

def ViewOldVersion(request, doc_id, delimiter, oldVersion):
	docs = Document.objects.filter(id=doc_id)
	for doc in docs:
		owner_id = doc.owner_id
		title = doc.title
		content = doc.content
		latestVersion = doc.version
	docHistory = History.objects.filter(doc_id=doc_id)
	versionHistory = History.objects.filter(doc_id=doc_id, version=oldVersion)
	for vh in versionHistory:
		versionHistory = vh
	changes = versionHistory.changes.split('/')
	updatedContent = content.split('/')
	for change in changes:
		updatedContent = updateContent(updatedContent, change.split('-'))
	return render(request, 'viewOldVersion.html', {
		'user_id': str(request.user.id),
		'owner_id': str(owner_id),
		'title': title,
		'doc_id': doc_id,
		'latestVersion': latestVersion,
		'viewingVersion': oldVersion,
    	'content': updatedContent,
    	'docHistory': docHistory,
    })

def updateContent(currentContent, changes):
	#print(currentContent, changes)
	op = changes[0]
	text = changes[1]
	lineNumber = int(changes[2])
	if op == 'add':
		firstHalf = currentContent[0:lineNumber-1]
		secondHalf = currentContent[lineNumber-1:]
		newContent = firstHalf + [text] + secondHalf
		return newContent
	elif op == 'delete':
		newContent = currentContent
		del newContent[lineNumber-1]
		return newContent
	elif op == 'update':
		newContent = currentContent
		newContent[lineNumber-1] = text
		return newContent
	else:
		print("Invalid content operation!")

def AddLine(request, doc_id):
	####  Adds to the end of the file
	if request.method == 'POST':
		form = AddLineForm(request.POST)
		if form.is_valid():
			docs = Document.objects.filter(id=doc_id)
			for doc in docs:
				oldContent = doc.content
				prevVersion = doc.version
			newContent = form.cleaned_data['newContent']
			if oldContent == "":
				lineToRemove = 1
				updatedContent = newContent
			else:
				lineToRemove = len(oldContent.split('/')) + 1
				updatedContent = oldContent + '/' + newContent
			Document.objects.filter(id=doc_id).update(content=updatedContent)
			Document.objects.filter(id=doc_id).update(version=prevVersion+1)
			changes = 'delete-' + newContent + '-' + str(lineToRemove)
			updateHistory(request, doc_id, changes, prevVersion)
			return HttpResponseRedirect('/documents/view/' + doc_id)
	else:
		form = AddLineForm()
	return render(request, 'addLine.html', {'form': form})
	####  Adds to a specific line number
	# if request.method == 'POST':
	# 	form = AddLineForm(request.POST)
	# 	if form.is_valid():
	# 		docs = Document.objects.filter(id=doc_id)
	# 		for doc in docs:
	# 			content = doc.content
	# 		content = content.split('/')
	# 		lineToAdd = form.cleaned_data['lineToAdd']
	# 		if len(content) == 1:
	# 			secondHalf = content
	# 			updatedContent = [form.cleaned_data['newContent']] + secondHalf
	# 			updatedContent = '/'.join(updatedContent)
	# 		else:
	# 			firstHalf = content[0:lineToAdd-1]
	# 			secondHalf = content[lineToAdd-1:]
	# 			updatedContent = firstHalf + [form.cleaned_data['newContent']] + secondHalf
	# 			updatedContent = '/'.join(updatedContent)
	# 		Document.objects.filter(id=doc_id).update(content=updatedContent)
	# 		return HttpResponseRedirect('/profile')
	# else:
	# 	form = AddLineForm()
	# return render(request, 'addLine.html', {'form': form})


def DeleteLine(request, doc_id):
	if request.method == 'POST':
		form = DeleteLineForm(request.POST)
		if form.is_valid():
			docs = Document.objects.filter(id=doc_id)
			for doc in docs:
				content = doc.content
				prevVersion = doc.version
			content = content.split('/')
			lineToDelete = form.cleaned_data['lineToDelete']
			lineToAdd = lineToDelete 								#for changes in history model
			contentToAdd = content[lineToAdd-1] 					#for changes in history model
			changes = 'add-' + contentToAdd + '-' + str(lineToAdd)  #for changes in history model
			del content[lineToDelete-1:lineToDelete]
			content = '/'.join(content)
			Document.objects.filter(id=doc_id).update(content=content)
			Document.objects.filter(id=doc_id).update(version=prevVersion+1)
			updateHistory(request, doc_id, changes, prevVersion)
			return HttpResponseRedirect('/documents/view/' + doc_id)
	else:
		form = DeleteLineForm()
	return render(request, 'deleteLine.html', {'form': form})

def UpdateLine(request, doc_id):
	if request.method == 'POST':
		form = UpdateLineForm(request.POST)
		if form.is_valid():
			docs = Document.objects.filter(id=doc_id)
			for doc in docs:
				content = doc.content
				prevVersion = doc.version
			content = content.split('/')
			lineToUpdate = form.cleaned_data['lineToUpdate']
			newContent = form.cleaned_data['newContent']
			oldContent = content[lineToUpdate-1]
			changes = 'update-' + oldContent + '-' + str(lineToUpdate)
			content[lineToUpdate-1] = newContent
			content = '/'.join(content)
			Document.objects.filter(id=doc_id).update(content=content)
			Document.objects.filter(id=doc_id).update(version=prevVersion+1)

			
			updateHistory(request, doc_id, changes, prevVersion)
			return HttpResponseRedirect('/documents/view/' + doc_id)
	else:
		form = UpdateLineForm()
	return render(request, 'updateLine.html', {'form': form})

def updateHistory(request, doc_id, changes, prevVersion):
	docHistory = History.objects.filter(doc_id=doc_id)
	for dh in docHistory:
		prevChanges = dh.changes
		prevUpdaters = dh.updater_ids
		History.objects.filter(id=dh.id).update(changes=changes + '/' + prevChanges)
		History.objects.filter(id=dh.id).update(updater_ids=str(request.user.id) + '/' + prevUpdaters)
	History.objects.create(doc_id=doc_id, version=prevVersion, changes=changes, updater_ids=str(request.user.id)) #to revert to this version <--, do these changes in sequence
	return

def ShareDoc(request, doc_id):
	usernames = getOuUsernames()
	if request.method == 'POST':
		form = ShareDocForm(request.POST)
		usernameSharedWith = request.POST.get('username-dropdown')
		usersSharedWith = CustomUser.objects.filter(username=usernameSharedWith)
		for user in usersSharedWith:
			user_id = user.id
		docs = Document.objects.filter(id=doc_id)
		for doc in docs:
			collaborators = doc.collaborators
		if collaborators == "":
			Document.objects.filter(id=doc_id).update(collaborators=str(user_id))
		else:
			Document.objects.filter(id=doc_id).update(collaborators=str(collaborators) + '/' + str(user_id))
		# content = content.split('/')
		# lineToUpdate = form.cleaned_data['lineToUpdate']
		# newContent = form.cleaned_data['newContent']
		# content[lineToUpdate-1] = newContent
		# content = '/'.join(content)
		# Document.objects.filter(id=doc_id).update(content=content)
		return HttpResponseRedirect('/profile')
	else:
		form = ShareDocForm()
	return render(request, 'shareDoc.html', {
		'usernames': usernames,
		})

# def Complain(request, doc_id, accused):
