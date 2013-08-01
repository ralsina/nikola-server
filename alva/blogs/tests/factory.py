"""Factory functions for creating models in test data preparation. This class 
in not intended to be used in business logic.
"""

from django.contrib.auth.models import User

from blogs.models import Blog

def create_author(username='author', password='secret', email='author@example.com'):
    return User.objects.create_user(username=username, password=password, email=email)

def create_blog(owner=None):
    owner = owner or create_author()
    blog, is_created = Blog.objects.get_or_create(owner=owner)
    return blog 

