from django.db import models
from users.models import CustomUser

# Create your models here.
class TabooWord(models.Model):
	suggested_by = models.CharField(default='', max_length=100)
	word = models.CharField(max_length=100, default='')
	is_taboo = models.BooleanField('Taboo Status', default=False)
	
	def __str__(self):
		return self.word