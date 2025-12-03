from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Tag

User = get_user_model()

class TaggingSearchTests(TestCase):
    def setUp(self):
        u = User.objects.create_user('user', 'u@example.com', 'pass')
        self.post1 = Post.objects.create(title='Django tips', slug='django-tips', content='learn django', author=u)
        self.post2 = Post.objects.create(title='Python news', slug='python-news', content='python 3.11', author=u)
        # using taggit or custom Tag adjust accordingly
        tag = Tag.objects.create(name='django', slug='django')
        self.post1.tags.add(tag)

    def test_posts_by_tag_view(self):
        url = reverse('posts_by_tag', kwargs={'tag_name': 'django'})
        resp = self.client.get(url)
        self.assertContains(resp, self.post1.title)
        self.assertNotContains(resp, self.post2.title)

    def test_search_title_and_tag(self):
        resp = self.client.get(reverse('post_search'), {'q': 'django'})
        self.assertContains(resp, self.post1.title)
