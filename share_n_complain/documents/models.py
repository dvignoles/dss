from django.db import models
from users.models import CustomUser

# Create your models here.
class Document(models.Model):
	owner = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	collaborators = models.CharField(max_length=100, default='')
	title = models.CharField(max_length=100, default='')
	content = models.CharField(max_length=10000, default='')
	private = models.BooleanField('Classification', default=False)
	version = models.IntegerField(default=1)
	
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