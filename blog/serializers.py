from .models import Articles, Tags, Comments
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Articles
        fields = [ 'id', 'title', 'body', 'status']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = [ 'id', 'tag_name']

class CommentSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField()
    class Meta:
        model = Comments
        fields = [ 'id', 'comments', 'article_id']