from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here
    interests = models.CharField(max_length=100, default='')
    is_OU = models.BooleanField('OU status', default=False)

    def __str__(self):
        return self.username