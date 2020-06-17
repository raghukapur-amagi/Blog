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
<<<<<<< HEAD
    slug = models.SlugField(max_length=140, unique=True)
    #slug = models.CharField(max_length= 10, unique = True)
=======
>>>>>>> parent of 07226ac... changed the article url formatting from localhost/article-id to localhost/article_title-article_slug
    status = models.CharField(
    choices = [('Publish',publish),('Draft',draft)],
        default = draft,
        max_length=20,
        )
    
    def __str__(self):
        return self.title
 
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

class Tags(BaseModel):
    tag_name = models.CharField(max_length = 100, unique=True)

class ArticleTagMapping(BaseModel):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)

class Comments(BaseModel):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    comments = models.TextField(null = False) 
