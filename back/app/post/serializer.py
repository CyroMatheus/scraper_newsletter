from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
    
    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            post.categories.add(category)
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)

        return post