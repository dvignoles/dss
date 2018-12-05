from django.db import models
from users.models import CustomUser

# Create your models here.
class Document(models.Model):
	owner = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	collaborators = models.CharField(max_length=100, default='')

	title = models.CharField(max_length=100, default='')
	content = models.CharField(max_length=10000, default='')

	#TODO: implement in views
	line_editors = models.CharField(default='')

	private = models.BooleanField('Classification', default=False)
	version = models.IntegerField(default=1)

	locked = models.BooleanField('Locked Status', default=False)
	locked_by = models.IntegerField(blank=True, null=True)
	
	def __str__(self):
		doc = [self.owner, self.collaborators, self.content]
		return doc

class History(models.Model):
	doc = models.ForeignKey(Document, null=False, on_delete=models.CASCADE)
	version = models.IntegerField(null=False)
	changes = models.CharField(max_length=100, null=False)
	updater_ids = models.CharField(max_length=100, null=False, default='')
	
	def __str__(self):
		history = 'doc id: ' + str(self.doc_id) + ' - version: ' + str(self.version)
		return history

class Complaints(models.Model):
	#Document Details
	doc = models.ForeignKey(Document, on_delete=models.CASCADE)
	line_number_choices = (,) #TODO: Populate with ('1','1'), ('2',2') etc. based on number of lines in doc

	line_number = models.IntegerField(choices=line_number_choices)

	#User Details
	accused = models.ForeignKey(CustomUser, on_delete=models.CASCADE)




	
