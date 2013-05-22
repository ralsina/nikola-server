from __future__ import unicode_literals, print_function

import codecs
from contextlib import contextmanager
import os

from django.db import models
from django.contrib.auth.models import User
from django.template import Context, loader

import django_rq

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

BASE_BLOG_PATH = "/tmp"


class Blog(models.Model):
    owner = models.ForeignKey(User, related_name="owner_of")
    members = models.ManyToManyField(User, related_name="member_of")
    name = models.CharField(max_length=64, unique=True)
    domain = models.CharField(max_length=64, unique=True, blank=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=500, blank=True)
    language = models.CharField(max_length=9, choices=LANGUAGE_CHOICES)
    dirty = models.BooleanField(default=False)

    def path(self):
        return os.path.join(BASE_BLOG_PATH, self.name)

    def url(self):
        if self.domain:
            return self.domain
        else:
            return self.name+".donewithniko.la"

    def save(self, *args, **kwargs):
        if not os.path.isdir(self.path()):
            init_blog.delay(self)
        save_blog_config.delay(self)
        build_blog.delay(self)
        self.dirty = True
        return super(Blog, self).save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User)
    blogs = models.ManyToManyField(Blog)
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    text = models.TextField(max_length=100000)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=512)
    description = models.TextField(max_length=1024)

class Story(Post):
    pass


# Tasks that are delegated to RQ

@django_rq.job
def init_blog(blog):
    """Create the initial structure of the blog."""
    blog_path = os.path.join("/tmp", blog.name)
    os.system("nikola init {0}".format(blog_path))

@django_rq.job
def save_blog_config(blog):
    config_path = os.path.join(blog.path(), "conf.py")
    with codecs.open(config_path, "wb+", "utf-8") as f:
        template = loader.get_template('blogs/conf.tmpl')
        context = Context(dict(
            BLOG_AUTHOR=" ".join([blog.owner.first_name, blog.owner.last_name]),
            BLOG_TITLE=blog.title,
            SITE_URL=blog.url(),
            BLOG_EMAIL=blog.owner.email,
            BLOG_DESCRIPTION=blog.description,
            DEFAULT_LANG=blog.language,
            ))
        data = template.render(context)
        print(data)
        f.write(data)

@django_rq.job
def build_blog(blog):
    with cd(blog.path()):
        os.system("nikola build")
        blog.dirty = False
        blog.save()

# Utility thingies

@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)
