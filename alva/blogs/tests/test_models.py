from datetime import datetime

from django.test import TestCase

from blogs.models import Story, Post
from blogs.tests import factory

class BaseTestCase(TestCase):
    def setUp(self):
        self.author = factory.create_author()
        self.blog = factory.create_blog(owner=self.author)
        
class TestStory(BaseTestCase):
    def test_create_story(self):
        data = {
            'blog': self.blog,
            'author': self.author,
            'date': datetime(2013,12,31, 00, 16),
            'description': '',
            'dirty': True,
            'markup': 'markdown',
            'slug': 'my-first-blog',
            'tags': 'life style, diary',
            'text': 'Papoy? Wha kind a papoy? No no no, paPOY! Ohhh, paPOY. He he he',
            'title': 'My first blog'
        }
        story = Story.objects.create(**data)
        self.assertIn(story, self.author.story_set.all())
        
class TestPost(BaseTestCase):
    def test_create_post(self):
        data = {
            'blog': self.blog,
            'author': self.author,
            'date': datetime(2013,12,31, 00, 16),
            'description': '',
            'dirty': True,
            'markup': 'markdown',
            'slug': 'my-first-blog',
            'tags': 'life style, diary',
            'text': 'Papoy? Wha kind a papoy? No no no, paPOY! Ohhh, paPOY. He he he',
            'title': 'My first blog'
        }
        post = Post.objects.create(**data)
        self.assertIn(post, self.author.post_set.all())
 
