from django.shortcuts import render

from .forms import SuggestTabooForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from users.models import CustomUser

from users.views import getOuUsernames


def SuggestTaboo(request):
    if request.method == 'POST':
        form = SuggestTabooForm(request.POST)
        if form.is_valid():
            tabooWord = form.save(commit=False)
            if request.user:
            	tabooWord.suggested_by = request.user.username
            else:
            	tabooWord.suggested_by = None
            tabooWord.save()
            #return HttpResponse('Your document ' + doc.title + ' was saved!')
            #return render(request, 'profile.html')
            return HttpResponseRedirect('/profile')
    else:
        form = SuggestTabooForm()
    return render(request, 'suggestTaboo.html', {
        'form': form
    })