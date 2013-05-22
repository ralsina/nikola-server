from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

# Create your models here.

class Blog(models.Model):
    owner = models.ForeignKey(User, related_name="owner_of")
    members = models.ManyToManyField(User, related_name="member_of")
    name = models.CharField(max_length=64, unique=True)
    domain = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=500, default="")
    language = models.CharField(max_length=9, choices=LANGUAGE_CHOICES)
    dirty = models.BooleanField(default=False)

class Post(models.Model):
    author = models.ForeignKey(User)
    blogs = models.ManyToManyField(Blog)
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    text = models.TextField(max_length=100000)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=512)
    description = models.TextField(max_length=1024)
    dirty = models.BooleanField(default=False)

class Story(Post):
    pass

