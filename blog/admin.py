from django.contrib import admin
from .models import (
    Blog,
    Comment
)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'title', 'content',
                    'creation_date', 'last_update_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'blog', 'content',
                    'creation_date']
