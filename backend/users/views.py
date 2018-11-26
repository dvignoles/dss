from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import CustomUser

class Apply(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'apply.html'

def getUsers():
	allUsers = CustomUser.objects.all()
	users = []
	for user in allUsers:
		users.append(user.username)
	return users