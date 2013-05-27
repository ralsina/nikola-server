# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Blog'
        db.create_table(u'blogs_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'owner_of', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('dirty', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blogs', ['Blog'])

        # Adding M2M table for field members on 'Blog'
        m2m_table_name = db.shorten_name(u'blogs_blog_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'blogs.blog'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', 'user_id'])

        # Adding model 'Post'
        db.create_table(u'blogs_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100000, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'blogs', ['Post'])

        # Adding M2M table for field blogs on 'Post'
        m2m_table_name = db.shorten_name(u'blogs_post_blogs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blogs.post'], null=False)),
            ('blog', models.ForeignKey(orm[u'blogs.blog'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'blog_id'])

        # Adding model 'Story'
        db.create_table(u'blogs_story', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['blogs.Post'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'blogs', ['Story'])


    def backwards(self, orm):
        # Deleting model 'Blog'
        db.delete_table(u'blogs_blog')

        # Removing M2M table for field members on 'Blog'
        db.delete_table(db.shorten_name(u'blogs_blog_members'))

        # Deleting model 'Post'
        db.delete_table(u'blogs_post')

        # Removing M2M table for field blogs on 'Post'
        db.delete_table(db.shorten_name(u'blogs_post_blogs'))

        # Deleting model 'Story'
        db.delete_table(u'blogs_story')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'blogs.blog': {
            'Meta': {'object_name': 'Blog'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'member_of'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'owner_of'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'blogs.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'blogs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blogs.Blog']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'blogs.story': {
            'Meta': {'object_name': 'Story', '_ormbases': [u'blogs.Post']},
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['blogs.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blogs']