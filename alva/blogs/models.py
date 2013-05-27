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
    domain = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=128, unique=True)
    language = models.CharField(max_length=9, choices=LANGUAGE_CHOICES, default='en')
    description = models.TextField(max_length=500, blank=True)
    dirty = models.BooleanField(default=False)

    def path(self):
        return os.path.join(BASE_BLOG_PATH, self.name)

    def url(self):
        if self.domain:
            return self.domain
        else:
            return self.name+".donewithniko.la"

    def save(self, *args, **kwargs):
        build = kwargs.pop("build", True)
        r=super(Blog, self).save(*args, **kwargs)
        if build:
            blog_sync.delay(self.id)
        return r

    def __unicode__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    date = models.DateTimeField()
    tags = models.CharField(max_length=512, blank=True)
    text = models.TextField(max_length=100000, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    dirty = models.BooleanField(default=True)

    folder = "posts"

    class Meta:
        unique_together = (('slug', 'blog'),)

    def path(self, blog):
        return os.path.join(blog.path(), self.folder, "%d.txt" % self.id)

    def _save_to_disk(self):
        with codecs.open(self.path(self.blog), "wb+", "utf8") as f:
            template = loader.get_template('blogs/post.tmpl')
            context = Context(dict(
                TITLE=self.title,
                DESCRIPTION=self.description,
                DATE=self.date.strftime('%Y/%m/%d %H:%M'),
                SLUG=self.slug,
                TAGS=self.tags,
                AUTHOR=" ".join([self.author.first_name, self.author.last_name]),
                TEXT=self.text,
                ))
            data = template.render(context)
            f.write(data)

    def save(self, *args, **kwargs):
        r = super(Post, self).save(*args, **kwargs)
        self._save_to_disk()
        return r

    def __unicode__(self):
        return "{0} ({1})".format(self.title, self.date.strftime('%Y-%m-%d %H:%M'))

class Story(Post):

    folder = "stories"


# Tasks that are delegated to RQ

@django_rq.job
def init_blog(blog_id):
    """Create the initial structure of the blog."""
    blog = Blog.objects.get(id=blog_id)
    blog_path = os.path.join("/tmp", blog.name)
    os.system("nikola init {0}".format(blog_path))

@django_rq.job
def save_blog_config(blog_id):
    blog = Blog.objects.get(id=blog_id)
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
        f.write(data)

@django_rq.job
def blog_sync(blog_id):
    """Dump the blog to disk, as smartly as possible."""
    needs_build = False
    blog = Blog.objects.get(id=blog_id)
    if not os.path.isdir(blog.path()):
        init_blog(blog_id)

    # FIXME: only do this if needed
    save_blog_config(blog_id)

    post_ids = set([])
    for post in blog.post_set.all():
        if post.dirty or not os.path.exists(post.path(post.blog)):
            needs_build = True
            post.dirty=False
            post.save()
            post_ids.add(post.id)
    post_folder = os.path.join(blog.path(), Post.folder)
    for fname in os.listdir(post_folder):
        if fname.split('.')[0] not in post_ids:
            needs_build = True
            os.unlink(os.path.join(post_folder, fname))

    build_blog(blog_id)

@django_rq.job
def build_blog(blog_id):
    blog = Blog.objects.get(id=blog_id)
    with cd(blog.path()):
        os.system("nikola build")
    blog.dirty = False
    blog.save(build=False)

# Utility thingies

@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)
