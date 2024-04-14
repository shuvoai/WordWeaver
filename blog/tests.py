from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.auth import get_user_model
from blog.models import Blog, Comment
from blog.views import BlogGenericViewSet, CommentGenericViewSet


User = get_user_model()


class BlogGenericViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
        self.blog = Blog.objects.create(
            user=self.user, title='Test Blog', content='Test Content')

    # authenticated user without the permission
    def test_list_blogs_authenticated_user(self):
        view = BlogGenericViewSet.as_view({'get': 'list'})
        request = self.factory.get('/blogs/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # authenticated user with the permission
    def test_list_blogs_with_permission(self):
        view = BlogGenericViewSet.as_view({'get': 'list'})
        request = self.factory.get('/blogs/')
        self.user.is_staff = True
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_blog(self):
        view = BlogGenericViewSet.as_view({'post': 'create'})
        request = self.factory.post(
            '/blogs/', {'user': self.user.id, 'title': 'New Blog', 'content': 'New Content'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_blog(self):
        view = BlogGenericViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/blogs/1/')
        force_authenticate(request, user=self.user)
        response = view(request, blog_id=self.blog.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_blog(self):
        view = BlogGenericViewSet.as_view({'put': 'update'})
        request = self.factory.put(
            '/blogs/1/', {'title': 'Updated Blog Title', 'content': 'Updated Content'})
        force_authenticate(request, user=self.user)
        response = view(request, blog_id=self.blog.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_blog(self):
        view = BlogGenericViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/blogs/3/')
        force_authenticate(request, user=self.user)
        response = view(request, blog_id=self.blog.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentGenericViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
        self.blog = Blog.objects.create(
            user=self.user, title='Test Blog', content='Test Content')
        self.comment = Comment.objects.create(
            author=self.user, blog=self.blog, content='Test Comment')

    def test_list_comments(self):
        view = CommentGenericViewSet.as_view({'get': 'list'})
        request = self.factory.get('/comments/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment(self):
        view = CommentGenericViewSet.as_view({'post': 'create'})
        data = {'author': self.user.id,
                'blog': self.blog.id, 'content': 'New Comment'}
        request = self.factory.post('/comments/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_comment(self):
        view = CommentGenericViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/comments/{self.comment.pk}/')
        force_authenticate(request, user=self.user)
        response = view(request, comment_id=self.comment.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        view = CommentGenericViewSet.as_view({'put': 'update'})
        data = {'content': 'Updated Comment Content'}
        request = self.factory.put(
            f'/comments/{self.comment.pk}/', data)
        force_authenticate(request, user=self.user)
        response = view(request, comment_id=self.comment.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_comment(self):
        view = CommentGenericViewSet.as_view({'patch': 'partial_update'})
        data = {'content': 'Partially Updated Comment Content'}
        request = self.factory.patch(
            f'/comments/{self.comment.pk}/', data)
        force_authenticate(request, user=self.user)
        response = view(request, comment_id=self.comment.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        view = CommentGenericViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(
            f'/comments/{self.comment.pk}/')
        force_authenticate(request, user=self.user)
        response = view(request, comment_id=self.comment.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
