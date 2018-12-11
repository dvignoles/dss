#### Models for database creation
#### Each Class is a model, each model has attributes which correspond to fields in the database
#### 	Update database with changes made to this file using 'python3 manage.py makemigrations' followed by 
####	'python3 manage.py migrate' on the command line.
#### Any time data from a model is needed during computations (updating content in a document, creating a document, etc.), 
#### 	models from this file must be imported at the top of that file
#### 	i.e. 'from app_name.models import ModelName'

from django.db import models
from users.models import CustomUser

class Document(models.Model):
	owner = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	collaborators = models.CharField(max_length=100, default='')

	title = models.CharField(max_length=100, default='')
	content = models.CharField(max_length=10000, default='')
	private = models.BooleanField('Private?', default=False)
	version = models.IntegerField(default=1)




	#ID of CustomUser who saved current document version
	updater_id = models.IntegerField(blank=True, null=True,default=0)





	locked = models.BooleanField('Locked Status', default=False)
	locked_by = models.IntegerField(blank=True, null=True)
	taboo_index = models.IntegerField(blank=True, null=True)

	def __str__(self):
		doc = 'owner: ' + str(self.owner) + 'collaborators: ' + self.collaborators + 'content: ' + self.content
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
	version = models.IntegerField(null=True)

	#User Details
	complainer = models.IntegerField(null=True)
	accused = models.IntegerField(null=True)

#Complaints about a Document Owner to SU
class Complaints_Owner(models.Model):
	doc = models.ForeignKey(Document, on_delete=models.CASCADE)
	complainer = models.IntegerField(null=True)
