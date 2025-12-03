# blog/tests/test_comments.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password123')
        self.user2 = User.objects.create_user(username='bob', password='password123')
        self.post = Post.objects.create(title='Test', body='Body', author=self.user)

    def test_create_comment_logged_in(self):
        self.client.login(username='alice', password='password123')
        url = reverse('posts:comment_new', kwargs={'post_id': self.post.pk})
        response = self.client.post(url, {'content': 'Nice post!'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(post=self.post, content='Nice post!', author=self.user).exists())

    def test_cannot_create_comment_anon(self):
        url = reverse('posts:comment_new', kwargs={'post_id': self.post.pk})
        response = self.client.post(url, {'content': 'Anon comment'})
        self.assertIn(response.status_code, (302, 403))  # likely redirect to login
        self.assertFalse(Comment.objects.filter(content='Anon comment').exists())

    def test_only_author_can_edit(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Original')
        self.client.login(username='bob', password='password123')
        url = reverse('posts:comment_edit', kwargs={'post_id': self.post.pk, 'pk': comment.pk})
        response = self.client.post(url, {'content': 'Hacked'}, follow=True)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Original')  # unchanged

    def test_author_can_delete(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='To be deleted')
        self.client.login(username='alice', password='password123')
        url = reverse('posts:comment_delete', kwargs={'post_id': self.post.pk, 'pk': comment.pk})
        response = self.client.post(url, follow=True)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
