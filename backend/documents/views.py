from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .forms import DocumentCreationForm, AddLineForm, DeleteLineForm, UpdateLineForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from documents.models import Document

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

def ViewDoc(request, title, doc_id, content):
	return render(request, 'viewDoc.html', {
		'title': title,
		'doc_id': doc_id,
    	'content': content.split('/'),
    })

def AddLine(request, doc_id):
	if request.method == 'POST':
		form = AddLineForm(request.POST)
		if form.is_valid():
			docs = Document.objects.filter(id=doc_id)
			for doc in docs:
				oldContent = doc.content
			newContent = form.cleaned_data['newContent']
			if oldContent == "":
				updatedContent = newContent
			else:
				updatedContent = oldContent + '/' + newContent
			Document.objects.filter(id=doc_id).update(content=updatedContent)
			return HttpResponseRedirect('/profile')
	else:
		form = AddLineForm()
	return render(request, 'addLine.html', {'form': form})

def DeleteLine(request, doc_id):
	if request.method == 'POST':
		form = DeleteLineForm(request.POST)
		if form.is_valid():
			docs = Document.objects.filter(id=doc_id)
			for doc in docs:
				content = doc.content
			content = content.split('/')
			lineToDelete = form.cleaned_data['lineToDelete']
			del content[lineToDelete-1:lineToDelete]
			content = '/'.join(content)
			Document.objects.filter(id=doc_id).update(content=content)
			return HttpResponseRedirect('/profile')
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
			content = content.split('/')
			lineToUpdate = form.cleaned_data['lineToUpdate']
			newContent = form.cleaned_data['newContent']
			content[lineToUpdate-1] = newContent
			content = '/'.join(content)
			Document.objects.filter(id=doc_id).update(content=content)
			return HttpResponseRedirect('/profile')
	else:
		form = UpdateLineForm()
	return render(request, 'updateLine.html', {'form': form})