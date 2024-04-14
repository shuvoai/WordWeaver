from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogManager(models.Manager):
    def create(self, *args, **kwargs):
        model_field_names = [field.name for field in self.model._meta.fields]
        valid_kwargs = {key: value for key,
                        value in kwargs.items() if key in model_field_names}
        blog = super(BlogManager, self).create(
            **valid_kwargs
        )
        return blog


class Blog(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name=_('user_blog'),
        verbose_name=_('User'),
        blank=False,
        null=False,
        help_text=_(
            'User who created this specific blog'
        ),
        error_messages={
            'null': _('User must be provided')
        }
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text=_("blog title"),
        verbose_name=_('title'),
        error_messages={
            'null': _('blog title must be provided')
        }
    )
    content = models.TextField(
        null=False,
        blank=False,
        help_text=_("blog content"),
        verbose_name=_('content'),
        error_messages={
            'null': _('blog content must be provided')
        }
    )
    creation_date = models.DateTimeField(
        verbose_name=_('creation date'),
        help_text=_("blog creation date"),
        auto_now_add=True
    )
    last_update_date = models.DateTimeField(
        help_text=_("blog last update date"),
        verbose_name=_('last update date'),
        null=True
    )
    objects = BlogManager()

    class Meta:
        ordering = ['-creation_date']


class CommentManager(models.Manager):
    def create(self, *args, **kwargs):
        model_field_names = [field.name for field in self.model._meta.fields]
        valid_kwargs = {key: value for key,
                        value in kwargs.items() if key in model_field_names}
        comment = super(CommentManager, self).create(
            **valid_kwargs
        )
        return comment


class Comment(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='author_comments',
        verbose_name=_('author'),
        blank=False,
        null=False,
        help_text=_('User who posted the comment'),
        error_messages={
            'null': _('author must be provided')
        }
    )
    blog = models.ForeignKey(
        to=Blog,
        on_delete=models.CASCADE,
        related_name='blog_comments',
        verbose_name=_('Blog'),
        blank=False,
        null=False,
        help_text=_('Blog to which the comment belongs to'),
        error_messages={
            'null': _('Blog must be provided')
        }
    )
    content = models.TextField(
        null=False,
        blank=False,
        help_text=_('Comment content'),
        verbose_name=_('Content'),
        error_messages={
            'null': _('Comment content must be provided')
        }
    )
    creation_date = models.DateTimeField(
        verbose_name=_('Creation date'),
        help_text=_('Comment creation date'),
        auto_now_add=True
    )
    last_update_date = models.DateTimeField(
        help_text=_("comment last update date"),
        verbose_name=_('last update date'),
        null=True
    )
    objects = CommentManager()

    class Meta:
        ordering = ['-creation_date']
