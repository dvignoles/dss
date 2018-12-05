from django.db import models
from users.models import CustomUser

# Create your models here.
class TabooWord(models.Model):
	word = models.CharField(max_length=100, default='')
	suggested_by = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	is_taboo = models.BooleanField('Taboo Status', default=False)
	
	def __str__(self):
		taboo_word = [self.word, self.suggested_by, self.is_taboo]
		return taboo_word