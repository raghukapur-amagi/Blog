from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Users(models.Model):
    username = models.CharField(validators=[MinLengthValidator(4)],max_length= 30,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null = True)
    email = models.EmailField()
    bio = models.TextField(null = True)
    password = models.CharField(validators=[MinLengthValidator(6)],max_length=30)
    created_at = models.TimeField(auto_now=False, auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)


class Articles(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    status = models.CharField(
    choices = [('Publish','Publish'),('Draft','Draft')],
        default = 'Draft',
        max_length=8,
        )
    created_at = models.TimeField(auto_now=False, auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

class Tags(models.Model):
    tag_name = models.CharField(max_length = 15, unique=True)
    created_at = models.TimeField(auto_now=False, auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

class Article_Tag_Mapping(models.Model):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now=False, auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

class Comments(models.Model):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    comments = models.TextField(null = False)
    created_at = models.TimeField(auto_now=False, auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)    
