from django.contrib.auth.models import AbstractUser
from django.db import models
import random as random

class CustomUser(AbstractUser):
    # add additional fields in here
    
    interests = models.CharField(max_length=100, default='')
    is_OU = models.BooleanField('OU status', default=False)
    prof_pic_num = models.IntegerField(default=random.randrange(20))
    ## share reqs attempt
    share_requests = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.username

# class UserShareRequests(models.Model):
#     user_id = models.IntegerField(null=False)
#     shared_by = models.IntegerField(null=False)
#     doc_id = models.IntegerField(null=False)

#     def __str__(self):
#         return ('user_id: ' + user_id + ' shared_by: ' + shared_by + ' doc_id: ' + doc_id)

    