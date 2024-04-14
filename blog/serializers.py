from django.contrib.auth import get_user_model
from rest_framework import serializers
from blog.models import (
    Blog,
    Comment
)
from django.utils import timezone

User = get_user_model()


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['pk', 'user', 'title', 'content',
                  'creation_date', 'last_update_date']
        read_only_fields = ['pk', 'creation_date', 'last_update_date']


class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['pk', 'user', 'title', 'content',
                  'creation_date', 'last_update_date']
        read_only_fields = ['pk', 'user', 'creation_date', 'last_update_date']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.last_update_date = timezone.now()
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'author', 'blog', 'content',
                  'creation_date']
        read_only_fields = ['pk', 'creation_date']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'author', 'blog', 'content',
                  'creation_date']
        read_only_fields = ['pk', 'author',
                            'blog', 'creation_date']

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.last_update_date = timezone.now()
        instance.save()
        return instance
