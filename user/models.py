from django.conf import settings
from django.db import models

class Users(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    bio = models.TextField(null = True)


