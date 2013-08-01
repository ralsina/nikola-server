# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import codecs
from contextlib import contextmanager
from datetime import datetime
import json
import os
import shutil
import time

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context, loader
import django_rq

from fileshack.models import Store

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Español'),
    ('ca', 'Català'),
    ('de', 'Deutsch'),
    ('el', 'Ελληνικά'),
    ('fa', 'فارسی'),
    ('fr', 'Français'),
    ('gr', 'Ελληνικά'),
    ('hr', 'Croatian'),
    ('it', 'Italiano'),
    ('ja', '日本語'),
    ('pl', 'polski'),
    ('ru', 'Русский'),
    ('pt_BR', 'Português'),
    ('tr_TR', 'Türkçe'),
    ('zh_CN', '简体中文'),
)

MARKUP_CHOICES = (
    ('rest', 'RestructuredText'),
    ('markdown', 'MarkDown'),
    ('textile', 'Textile'),
)

THEME_CHOICES = (
    "blogtxt",
    "default",
    "default_amelia",
    "default_cerulean",
    "default_cosmo",
    "default_cyborg",
    "default_flatly",
    "default_journal",
    "default_readable",
    "default_simplex",
    "default_slate",
    "default_spacelab",
    "default_spruce",
    "default_superhero",
    "default_united",
    "jinja-default",
    "jinja-default_amelia",
    "jinja-default_cerulean",
    "jinja-default_cosmo",
    "jinja-default_cyborg",
    "jinja-default_flatly",
    "jinja-default_journal",
    "jinja-default_readable",
    "jinja-default_simplex",
    "jinja-default_slate",
    "jinja-default_spacelab",
    "jinja-default_spruce",
    "jinja-default_superhero",
    "jinja-default_united",
    "jinja-site",
    "monospace",
    "orphan",
    "readable",
    "readable_amelia",
    "readable_cerulean",
    "readable_cosmo",
    "readable_cyborg",
    "readable_flatly",
    "readable_journal",
    "readable_readable",
    "readable_simplex",
    "readable_slate",
    "readable_spacelab",
    "readable_spruce",
    "readable_superhero",
    "readable_united",
    "site",
    "site-reveal",
    "site_amelia",
    "site_cerulean",
    "site_cosmo",
    "site_cyborg",
    "site_flatly",
    "site_journal",
    "site_readable",
    "site_simplex",
    "site_slate",
    "site_spacelab",
    "site_spruce",
    "site_superhero",
    "site_united",
)
THEME_CHOICES = [(x,x) for x in THEME_CHOICES]

BASE_BLOG_PATH = getattr(settings, "BASE_BLOG_PATH", "/tmp/blogs")
BASE_OUTPUT_PATH = getattr(settings, "BASE_OUTPUT_PATH", "/tmp/sites")
URL_SUFFIX = getattr(settings, "URL_SUFFIX", "donewithniko.la:80")
BACKUP_OUTPUT_PATH = os.path.join(getattr(settings, "MEDIA_ROOT", ""), "backups")


class Blog(models.Model):
    owner = models.ForeignKey(User, related_name="owner_of")
    members = models.ManyToManyField(User, related_name="member_of", blank=True, null=True)
    galleries = models.ForeignKey(Store, related_name="blog_gallery", null=True)
    static = models.ForeignKey(Store, related_name="blog_static", null=True)
    stores = models.ManyToManyField(Store, null=True)
    name = models.CharField(max_length=64, unique=True)
    domain = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=128, unique=True)
    language = models.CharField(max_length=9, choices=LANGUAGE_CHOICES, default='en')
    theme = models.CharField(max_length=64, choices=THEME_CHOICES, default='site')
    description = models.TextField(max_length=500, blank=True)
    dirty = models.BooleanField(default=False)

    def path(self):
        return os.path.join(BASE_BLOG_PATH, self.name)

    def output_path(self):
        return os.path.join(BASE_OUTPUT_PATH, self.name + URL_SUFFIX)

    def url(self):
        if self.domain:
            return "http://"+self.domain
        else:
            return "http://"+self.name+".donewithniko.la"

    def save(self, *args, **kwargs):
        r=super(Blog, self).save(*args, **kwargs)
        if not self.static:  # No static file store, add one
            path = "%s/%s" % (self.id, "files")
            store = Store(path=path)
            store.save()
            self.static = store
            r=super(Blog, self).save(*args, **kwargs)
        if not self.galleries:  # No static galleries store, add one
            path = "%s/%s" % (self.id, "galleries")
            store = Store(path=path)
            store.save()
            self.galleries = store
            r=super(Blog, self).save(*args, **kwargs)
        r=super(Blog, self).save(*args, **kwargs)
        blog_sync.delay(self.id)
        return r

    def __unicode__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    date = models.DateTimeField()
    tags = models.CharField(max_length=512, blank=True)
    text = models.TextField(max_length=100000, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    dirty = models.BooleanField(default=True)
    markup = models.CharField(max_length=30, choices=MARKUP_CHOICES, default='rest')

    folder = "posts"

    class Meta:
        unique_together = (('slug', 'blog'),)
        ordering = ['-date']

    def path(self):
        return os.path.join(self.blog.path(), self.folder, "%d.%s" % (self.id, self.markup))

    def url(self):
        return ('/'.join([self.blog.url(), self.folder, self.slug + '.html']))

    def save_to_disk(self):
        template = loader.get_template('blogs/%s.tmpl' % self.markup)
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
        with codecs.open(self.path(), "wb+", "utf8") as f:
            f.write(data)

    def save(self, *args, **kwargs):
        r = super(Post, self).save(*args, **kwargs)
        if self.dirty:
            if self.date <= datetime.now():
                self.blog.dirty = True
                self.blog.save()
            else:
                scheduler = django_rq.get_scheduler('default')
                scheduler.enqueue_at(
                    self.date,
                    blog_sync.delay,
                    kwargs={'blog_id': self.blog.id}
                )
        return r

    def __unicode__(self):
        return "{0} ({1}) in {2}".format(self.title, self.date.strftime('%Y-%m-%d %H:%M'), self.blog)

class Story(Post):

    folder = "stories"


# Tasks that are delegated to RQ

@django_rq.job
def backup_blog(blog_id):
    blog = Blog.objects.get(id=blog_id)
    path = blog.path()
    fname = "%s.zip" % blog.name
    if not os.path.isdir(BACKUP_OUTPUT_PATH):
        os.makedirs(BACKUP_OUTPUT_PATH)
    fname = os.path.join(BACKUP_OUTPUT_PATH, fname)
    subprocess.check_call(["zip", fname, path, "-r"])


@django_rq.job
def init_blog(blog):
    """Create the initial structure of the blog."""
    os.system("nikola init {0}".format(blog.path()))

@django_rq.job
def blog_sync(blog_id):
    """Dump the blog to disk, as smartly as possible."""
    needs_build = False
    blog = Blog.objects.get(id=blog_id)
    if not os.path.isdir(blog.path()):
        init_blog(blog)
        needs_build = True

    needs_build = True
    save_blog_config(blog)

    _syncronize_database_with_files(blog, blog.post_set.all(), Post.folder)
    _syncronize_database_with_files(blog, blog.story_set.all(), Story.folder)

    stores = [blog.galleries, blog.static] + list(blog.stores.all())
    for s in stores:
        dst_dir = os.path.join(blog.path(), *(s.path.split('/')[1:]))
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)  # FIXME: handle this being a file
        file_names = set([])
        for i in s.items.all():
            src = i.fileobject.path
            fname = os.path.basename(src)
            dst = os.path.join(dst_dir, fname)
            file_names.add(fname)
            if not os.path.isfile(dst) or os.stat(dst).st_mtime < os.stat(src).st_mtime:
                shutil.copy(src, dst)
                needs_build = True

        real_files = set(os.listdir(dst_dir))
        for fname in (real_files - file_names):
            fname = os.path.join(dst_dir, fname)
            if os.path.isfile(fname):
                os.unlink(fname)
                needs_build = True

    if needs_build:
        build_blog(blog_id)


def _syncronize_database_with_files(blog, content_list, folder):
    content_ids = _generate_files_for_new_content(content_list)
    _remove_deleted_content(blog, content_ids, folder)


def _generate_files_for_new_content(content_list):
    content_ids = set([])
    for content in content_list:
        content_ids.add(str(content.id))
        if content.dirty or not os.path.exists(content.path()):
            needs_build = True
            content.dirty = False
            content.save_to_disk()
    return content_ids


def _remove_deleted_content(blog, content_ids, folder):
    content_folder = os.path.join(blog.path(), folder)
    for fname in os.listdir(content_folder):
        if fname.split('.')[0] not in content_ids:
            needs_build = True
            os.unlink(os.path.join(content_folder, fname))


def build_blog(blog_id):
    blog = Blog.objects.get(id=blog_id)
    with cd(blog.path()):
        os.system("nikola build")
        # This is not yet available on any Nikola release
        os.system("nikola check --clean-files")


def save_blog_config(blog):
    config_path = os.path.join(blog.path(), "conf.py")
    conf_data_path = os.path.join(blog.path(), "conf.json")
    with codecs.open(config_path, "wb+", "utf-8") as f:
        template = loader.get_template('blogs/conf.tmpl')
        context = Context()
        data = template.render(context)
        f.write(data)
    with codecs.open(conf_data_path, "wb+", "utf-8") as f:
        data = json.dump(dict(
            BLOG_AUTHOR=" ".join([blog.owner.first_name, blog.owner.last_name]),
            BLOG_TITLE=blog.title,
            SITE_URL=blog.url(),
            BLOG_EMAIL=blog.owner.email,
            BLOG_DESCRIPTION=blog.description,
            DEFAULT_LANG=blog.language,
            OUTPUT_FOLDER=blog.output_path(),
            THEME=blog.theme,
            ), f, skipkeys=True, sort_keys=True)


# Utility thingies

@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)
