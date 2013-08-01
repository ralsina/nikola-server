from django.contrib.auth.models import User

from blogs.models import Blog

def create_author(username='author', password='secret', email='author@example.com'):
    return User.objects.create_user(username=username, password=password, email=email)

def create_blog(owner=None):
    owner = owner or create_author()
    return Blog.objects.get_or_create(owner=owner)

