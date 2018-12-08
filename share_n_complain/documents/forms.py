#### Forms for various user input
####	i.e. document edits (add, delete, update) and sharing
#### Linked to from documents/views.py (AddLine, DeleteLine, UpdateLine, and ShareDoc functions)

from django import forms
from .models import Document, Complaints

# Renders a form with fields which correspond to attributes 'title' and 'private' inherited from the Document model
class DocumentCreationForm(forms.ModelForm):
	private = forms.BooleanField(label='Private?', required=False)
	class Meta:
		model = Document
		fields = ('title','private')

class AddLineForm(forms.Form):
	####  Adds to a specific line number
	#lineToAdd = forms.IntegerField(label='Add Line #', max_value=1000000)
	newContent = forms.CharField(label='New Content', max_length=100)

class DeleteLineForm(forms.Form):
	lineToDelete = forms.IntegerField(label='Delete Line #', max_value=1000000)

class UpdateLineForm(forms.Form):
	lineToUpdate = forms.IntegerField(label='Update Line #', max_value=1000000)
	newContent = forms.CharField(label='New Content', max_length=100)

class ShareDocForm(forms.Form):
	shareWith = forms.CharField(label='Share with', max_length=100)
