from django.shortcuts import render

from .forms import SuggestTabooForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import TabooWord
from users.models import CustomUser

from users.views import getOuUsernames


def SuggestTaboo(request):
    if request.method == 'POST':
        form = SuggestTabooForm(request.POST)
        if form.is_valid():
            tabooWord = form.save(commit=False)
            if request.user.is_anonymous:
                tabooWord.suggested_by = "Guest"
            else:
            	tabooWord.suggested_by = request.user.username
            tabooWord.save()
            #return HttpResponse('Your document ' + doc.title + ' was saved!')
            #return render(request, 'profile.html')
            return HttpResponseRedirect('/profile')
    else:
        form = SuggestTabooForm()
    return render(request, 'suggestTaboo.html', {
        'form': form
    })

def getTabooList():
    allTaboo = TabooWord.objects.all()
    tabooList = []
    for taboo in allTaboo:
        if taboo.is_taboo:
            tabooList.append(taboo.word)
    return tabooList