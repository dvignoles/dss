from django import forms
from .models import Document

class DocumentCreationForm(forms.ModelForm):
	private = forms.BooleanField(label='Private?', required=False)
	class Meta:
		model = Document
		fields = ('title','private')

	# def __init__(self, *args, **kwargs):
	# 	super(DocumentCreationForm, self).__init__(*args, **kwargs)
	# 	self.fields['owner'].initial = self.owner_id

# class DocumentCreationForm(forms.ModelForm):
# 	class Meta:
# 		model = Document
# 		fields = ('content', 'owner')

# 	def __init__(self, *args, **kwargs):
# 	    request = kwargs.pop('request')
# 	    super(DocumentCreationForm, self).__init__(*args, **kwargs)
# 	    self.fields['owner'].initial = request.user.id
# 	    #self.save()
# #	    print(request.user.id)

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