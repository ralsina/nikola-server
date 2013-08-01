from django.test import TestCase

from blogs.forms import PostForm, StoryForm
from blogs.models import Post, Story
from blogs.tests import factory


class TestPostForm(TestCase):
    def setUp(self):
        factory.create_blog()

    def test_post_form_is_for_post_model(self):
        self.assertEqual(Post, PostForm.Meta.model)
        
    def test_empty_form_is_not_valid(self):
        form = PostForm() 
        self.assertFalse(form.is_valid())

    def test_post_valid_form(self):
        data = {
            'blog': 1,
            'date_0': '01/08/2013 09:20',
            'description': '',
            'dirty': True,
            'markup': 'markdown',
            'slug': 'my-first-blog',
            'tags': 'life style, diary',
            'text': 'Papoy? Wha kind a papoy? No no no, paPOY! Ohhh, paPOY. He he he',
            'title': 'My first blog'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())


class TestPostStory(TestCase):
    def setUp(self):
        factory.create_blog()

    def test_story_form_is_for_story_model(self):
        self.assertEqual(Story, StoryForm.Meta.model)
        
    def test_empty_form_is_not_valid(self):
        form = StoryForm() 
        self.assertFalse(form.is_valid())

