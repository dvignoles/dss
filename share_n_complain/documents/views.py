#### Views are where most of the logic is stored.  When a user accessess a path in documents/urls.py, the 
#### 	corresponding view function in this file is called.  From there, the view function renders a specific template 
####	from templates/ (The template stores the html code that the user sees in the browser).


from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .forms import DocumentCreationForm, AddLineForm, DeleteLineForm, UpdateLineForm, ShareDocForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from documents.models import Document, History, Complaints
from users.models import CustomUser
from taboo.models import TabooWord

from users.views import getOuUsernames
from taboo.views import getTabooList


# Creates a document by passing the DocumentCreationForm (located in documents/forms.py) into templates/createDoc.html 
def CreateDoc(request):
    if request.method == 'POST':
        form = DocumentCreationForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
			
            doc.save()
            return HttpResponseRedirect('/profile')
    else:
        form = DocumentCreationForm()
    return render(request, 'createDoc.html', {
        'form': form
    })

# When the user locks/unlocks a document, this function updates that document's 'locked' and 'locked_by' attributes in the database,
# 	and then returns the user to the document via documents/view/doc_id.
def ChangeLockedStatus(request, doc_id):
	docs = Document.objects.filter(id=doc_id)
	for doc in docs:
		if doc.locked:
			Document.objects.filter(id=doc_id).update(locked=0)
		else:
			Document.objects.filter(id=doc_id).update(locked=1, locked_by=request.user.id)
		return HttpResponseRedirect('/documents/view/' + doc_id)

#save relevant doc information in current session
def doc_session_set(request, doc_id, old_version, version_id = -1):
	request.session['current_doc'] = doc_id
	this_doc = Document.objects.get(id=doc_id)
	request.session['current_doc_owner'] = this_doc.owner.id

	if old_version == False:
		request.session['current_doc_version'] = this_doc.version
		request.session['current_doc_last_updater'] = this_doc.updater_id
	else:
		request.session['current_doc_version'] = version_id
		versionHistory = History.objects.get(doc_id=doc_id, version=version_id)
		versionUpdaterId= versionHistory.updater_ids[-1]
		request.session['current_doc_last_updater'] = versionUpdaterId
		
# Passes information about a specific document, the taboo list, and the document's history into templates/viewDoc.html
def ViewDoc(request, doc_id):
	doc_session_set(request, doc_id,old_version=False)

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
	content = content.split('/')
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
	tabooList = getTabooList()
	for index, value in enumerate(content): 		# Checks if document contains a taboo word. If so, 'hasTaboo' attribute of that
		if value in tabooList:						# 	document is updated to True
			hasTaboo = True
			tabooIndex = index
			break
		else:
			hasTaboo = False
			tabooIndex = None
	Document.objects.filter(id=doc_id).update(taboo_index=tabooIndex)

	#ID of last persion to update document
	updater_id = Document.objects.get(id=doc_id).updater_id

	if(updater_id != 0):
		updater_name = CustomUser.objects.get(id=updater_id).username
	else:
		updater_name = 'NA'


	is_OU = request.user.is_OU

	return render(request, 'viewDoc.html', {
		'user_id': str(request.user.id),
		'is_OU':is_OU,
		'owner_id': str(owner_id),
		'title': title,
		'private': private,
		'doc_id': doc_id,
    	'content': content,
    	'is_collaborator': is_collaborator,
    	'version': version,
    	'docHistory': docHistory,
    	'locked': locked,
    	'locked_by': str(locked_by),
    	'editor': editor,
    	'tabooList': tabooList,
    	'hasTaboo': hasTaboo,
    	'tabooIndex': tabooIndex,
		'updater_id' : updater_id,
		'updater_name': updater_name
    })

# Takes changes (from History model) needed to achieve 'oldVersion' of a document with id 'doc_id' and applies them using 
# 	the helper function updateContent() below.
def ViewOldVersion(request, doc_id, delimiter, oldVersion):
	doc_session_set(request,doc_id,old_version=True,version_id=oldVersion)
	
	docs = Document.objects.filter(id=doc_id)
	for doc in docs:
		owner_id = doc.owner_id
		title = doc.title
		content = doc.content
		latestVersion = doc.version
	docHistory = History.objects.filter(doc_id=doc_id)
	versionHistory = History.objects.filter(doc_id=doc_id, version=oldVersion)

	#Get Updater Username for this Version History
	versionHistoryEntry = versionHistory[0]
	versionUpdaterId= versionHistoryEntry.updater_ids[-1]
	versionUpdaterName = CustomUser.objects.get(id=versionUpdaterId).username

	for vh in versionHistory:
		versionHistory = vh
	changes = versionHistory.changes.split('/')
	updatedContent = content.split('/')
	for change in changes:													# updates current content to previous version
		updatedContent = updateContent(updatedContent, change.split('-'))
	return render(request, 'viewOldVersion.html', {
		'user_id': str(request.user.id),
		'is_OU': request.user.is_OU,
		'owner_id': str(owner_id),
		'title': title,
		'doc_id': doc_id,
		'latestVersion': latestVersion,
		'viewingVersion': oldVersion,
    	'content': updatedContent,
    	'docHistory': docHistory,
		'updater_id':versionUpdaterId,
		'updater':versionUpdaterName
    })

# Helper function for rolling back document content to previous version
def updateContent(currentContent, changes):
	op = changes[0] 				# operation to execute (add, delete, or update)
	text = changes[1] 				# text content to add or update
	lineNumber = int(changes[2]) 	# line number on which to do operation (uses 1-indexing, must be converted to 0-indexing, as below)
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

# Recycles AddLineForm to update a taboo line to some new content
# 	grabs the taboo_index from the Document model and updates the newContent to that index of the oldContent
#	also updates the History model
def FixTaboo(request, doc_id):
	if request.method == 'POST':
		form = AddLineForm(request.POST)
		if form.is_valid():
			docs = Document.objects.filter(id=doc_id)
			for doc in docs:
				oldContent = doc.content
				prevVersion = doc.version
				tabooIndex = doc.taboo_index
			newContent = form.cleaned_data['newContent']
			oldContent = oldContent.split('/')
			changes = 'update-' + oldContent[tabooIndex] + '-' + str(tabooIndex+1)
			oldContent[tabooIndex] = newContent
			updatedContent = '/'.join(oldContent)
			Document.objects.filter(id=doc_id).update(content=updatedContent)
			Document.objects.filter(id=doc_id).update(version=prevVersion+1)
			updateHistory(request, doc_id, changes, prevVersion)
			return HttpResponseRedirect('/documents/view/' + doc_id)
	else:
		form = AddLineForm()
	return render(request, 'addLine.html', {'form': form})

# Adds a line to the end of a document using the AddLine form in documents/forms.py
# Renders the updated document by redirecting to documents/view/doc_id
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

			#keep track of last user
			Document.objects.filter(id=doc_id).update(updater_id = request.user.id)

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

# Deletes a specific line of a document via DeleteLineForm in documents/forms.py
# Renders the updated document by redirecting to documents/view/doc_id
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


			#keep track of last user
			Document.objects.filter(id=doc_id).update(updater_id = request.user.id)


			updateHistory(request, doc_id, changes, prevVersion)
			return HttpResponseRedirect('/documents/view/' + doc_id)
	else:
		form = DeleteLineForm()
	return render(request, 'deleteLine.html', {'form': form})

# Updates a specific line of a document to new content via UpdateLineForm in documents/forms.py
# Renders the updated document by redirecting to documents/view/doc_id
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
			#keep track of last user
			Document.objects.filter(id=doc_id).update(updater_id = request.user.id)
			
			updateHistory(request, doc_id, changes, prevVersion)
			return HttpResponseRedirect('/documents/view/' + doc_id)
	else:
		form = UpdateLineForm()
	return render(request, 'updateLine.html', {'form': form})

# Helper function to update the History model whenever a document is changed
def updateHistory(request, doc_id, changes, prevVersion):
	docHistory = History.objects.filter(doc_id=doc_id)
	for dh in docHistory:
		prevChanges = dh.changes
		prevUpdaters = dh.updater_ids
		History.objects.filter(id=dh.id).update(changes=changes + '/' + prevChanges)
		History.objects.filter(id=dh.id).update(updater_ids=str(request.user.id) + '/' + prevUpdaters)
	History.objects.create(doc_id=doc_id, version=prevVersion, changes=changes, updater_ids=str(request.user.id)) #to revert to this version <--, do these changes in sequence
	return

# Allows users to share a document using ShareDocForm from documents/forms.py
# The 'collaborators' attribute of the document is updated to include the user_id with whom the document was shared
# Redirects ti the current user's profile page
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

def Complain(request, doc_id):
	complainer = request.user.id
	doc = Document.objects.get(id=request.session['current_doc'])
	version = request.session['current_doc_version']
	accused = request.session['current_doc_last_updater']

	c = Complaints(doc=doc,version=version,complainer=complainer,accused=accused)
	c.save()

	request.session.flush()
	context = {}
	return render(request,'complain.html', context)