from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class BlogTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(email='superuser@example.com', password='superpassword')
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content')

    def test_superuser_can_create_post(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_user_cannot_create_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-list')
        data = {'post': self.post.id, 'content': 'Test Comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_unauthenticated_user_cannot_comment(self):
        url = reverse('comment-list')
        data = {'post': self.post.id, 'content': 'Test Comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_delete_own_comment(self):
        self.client.force_authenticate(user=self.user)
        comment = Comment.objects.create(post=self.post, user=self.user, content='User Comment')
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_user_cannot_delete_others_comment(self):
        self.client.force_authenticate(user=self.user)
        other_user = User.objects.create_user(email='otheruser@example.com', password='otherpassword')
        comment = Comment.objects.create(post=self.post, user=other_user, content='Other User Comment')
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)
