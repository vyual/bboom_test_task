from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Post
from .serializers import UserSerializer, PostSerializer


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email="test@test.com", password='testpass')
        self.post = Post.objects.create(user=self.user, title='Test Post', body='This is a test post.')

    def test_create_post(self):
        self.client.login(username="testuser", password='testpass')
        data = {'user': self.user.id, 'title': 'New Post', 'body': 'This is a new post.'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_users(self):
        self.client.login(username="testuser", password='testpass')
        response = self.client.get('/api/users/')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_posts(self):
        self.client.login(username="testuser", password='testpass')
        response = self.client.get(f'/api/users/{self.user.id}/posts/')
        posts = Post.objects.filter(user=self.user.id)
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(f'/api/posts/{self.post.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, title='Test Post', body='This is a test post.')

    def test_user_list_view(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_posts/user_list.html')

    def test_user_posts_list_view(self):
        response = self.client.get(reverse('user-posts-list', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_posts/user_posts_list.html')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-create'), {'title': 'New Post', 'body': 'This is a new post.'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-posts-list', args=[self.user.id]))

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Пост успешно удален.')
