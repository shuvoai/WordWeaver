from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from users.views import UserGenericViewSet

User = get_user_model()


class UserGenericViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword'
        )
        self.admin_user = User.objects.create_user(
            username='admin', email='admin@example.com', password='adminpassword', is_staff=True
        )

    def test_list_users_as_admin(self):
        view = UserGenericViewSet.as_view({'get': 'list'})
        request = self.factory.get('/users/')
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_unauthenticated(self):
        view = UserGenericViewSet.as_view({'get': 'list'})
        request = self.factory.get('/users/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        view = UserGenericViewSet.as_view({'post': 'create'})
        data = {'username': 'newuser', 'password': 'newpassword12456',
                'email': 'newuser@example.com'}
        request = self.factory.post('/users/', data=data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user(self):
        view = UserGenericViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/users/{self.user.pk}/')
        force_authenticate(request, user=self.user)
        response = view(request, user_id=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        view = UserGenericViewSet.as_view({'put': 'update'})
        data = {'first_name': 'Updated First Name'}
        request = self.factory.put(f'/users/{self.user.pk}/', data=data)
        force_authenticate(request, user=self.user)
        response = view(request, user_id=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_user(self):
        view = UserGenericViewSet.as_view({'patch': 'partial_update'})
        data = {'last_name': 'Updated Last Name'}
        request = self.factory.patch(f'/users/{self.user.pk}/', data=data)
        force_authenticate(request, user=self.user)
        response = view(request, user_id=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        view = UserGenericViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/users/{self.user.pk}/')
        force_authenticate(request, user=self.user)
        response = view(request, user_id=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
