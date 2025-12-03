from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post


User = get_user_model()




class PostViewTests(TestCase):
def setUp(self):
self.user = User.objects.create_user(username='author', password='pass')
self.other = User.objects.create_user(username='other', password='pass')
self.post = Post.objects.create(
title='Test post', content='Body here', author=self.user
)


def test_list_view(self):
resp = self.client.get(reverse('posts:post-list'))
self.assertEqual(resp.status_code, 200)
self.assertContains(resp, self.post.title)


def test_detail_view(self):
resp = self.client.get(reverse('posts:post-detail', kwargs={'pk': self.post.pk}))
self.assertEqual(resp.status_code, 200)
self.assertContains(resp, self.post.content)


def test_create_requires_login(self):
resp = self.client.get(reverse('posts:post-create'))
self.assertNotEqual(resp.status_code, 200)


self.client.login(username='author', password='pass')
resp = self.client.post(reverse('posts:post-create'), {
'title': 'New', 'content': 'New body'
})
self.assertEqual(resp.status_code, 302) # redirect after success


def test_update_by_non_author_denied(self):
self.client.login(username='other', password='pass')
resp = self.client.get(reverse('posts:post-update', kwargs={'pk': self.post.pk}))
# Should redirect or return 403 depending on your mixin behavior
self.assertNotEqual(resp.status_code, 200)


def test_delete_by_author(self):
self.client.login(username='author', password='pass')
resp = self.client.post(reverse('posts:post-delete', kwargs={'pk': self.post.pk}))
self.assertEqual(resp.status_code, 302)
self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
