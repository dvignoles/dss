from django.db import models
from users.models import CustomUser

# Create your models here.
class Document(models.Model):
	owner = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	collaborators = models.CharField(max_length=100, default='')
	title = models.CharField(max_length=100, default='')
	content = models.CharField(max_length=10000, default='')
	private = models.BooleanField('Classification', default=False)
	
	def __str__(self):
		doc = [self.owner, self.collaborators, self.content]
		return doc