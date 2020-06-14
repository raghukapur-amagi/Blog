from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    class Meta:
        abstract = True

class Articles(BaseModel):
    publish = "Publish"
    draft = "Draft"
    user = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(
    choices = [('Publish',publish),('Draft',draft)],
        default = draft,
        max_length=20,
        )

class Tags(BaseModel):
    tag_name = models.CharField(max_length = 100, unique=True)

class Article_Tag_Mapping(BaseModel):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)

class Comments(BaseModel):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    comments = models.TextField(null = False) 
