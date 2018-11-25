from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .forms import DocumentCreationForm
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