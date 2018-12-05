from django import forms
from .models import TabooWord

class SuggestTabooForm(forms.ModelForm):
	class Meta:
		model = TabooWord
		fields = ('word',)