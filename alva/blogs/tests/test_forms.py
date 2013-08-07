from django.test import TestCase

from blogs.forms import PostForm, StoryForm
from blogs.models import Post, Story
from blogs.tests import factory


class BaseTestCase(TestCase):
    data = {
        'blog': 1,
        'date_0': '31/12/2013 00:16',
        'description': '',
        'dirty': True,
        'markup': 'markdown',
        'slug': 'my-first-blog',
        'tags': 'life style, diary',
        'text': 'Papoy? Wha kind a papoy? No no no, paPOY! Ohhh, paPOY. He he he',
        'title': 'My first blog'
    }

    def setUp(self):
        factory.create_blog()


class TestPostForm(BaseTestCase):
    def test_post_form_is_for_post_model(self):
        self.assertEqual(Post, PostForm.Meta.model)
        
    def test_empty_form_is_not_valid(self):
        form = PostForm() 
        self.assertFalse(form.is_valid())

    def test_create_valid_post_on_newyear_eve(self):
        form = PostForm(data=self.data)
        self.assertTrue(form.is_valid())


class TestPostStory(BaseTestCase):
    def test_story_form_is_for_story_model(self):
        self.assertEqual(Story, StoryForm.Meta.model)
        
    def test_empty_form_is_not_valid(self):
        form = StoryForm() 
        self.assertFalse(form.is_valid())

    def test_create_valid_story_on_newyear_eve(self):
        data = self.data.copy()
        data['date'] = '12/31/2013 00:16'
        form = StoryForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

