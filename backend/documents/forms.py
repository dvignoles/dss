from django import forms
from .models import Document

class DocumentCreationForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('title',)

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