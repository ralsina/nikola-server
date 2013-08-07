# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field stores on 'Blog'
        m2m_table_name = db.shorten_name(u'blogs_blog_stores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'blogs.blog'], null=False)),
            ('store', models.ForeignKey(orm[u'fileshack.store'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', 'store_id'])


    def backwards(self, orm):
        # Removing M2M table for field stores on 'Blog'
        db.delete_table(db.shorten_name(u'blogs_blog_stores'))


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
            'galleries': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'blog_gallery'", 'null': 'True', 'to': u"orm['fileshack.Store']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'en'", 'max_length': '9'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'member_of'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'owner_of'", 'to': u"orm['auth.User']"}),
            'static': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'blog_static'", 'null': 'True', 'to': u"orm['fileshack.Store']"}),
            'stores': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fileshack.Store']", 'null': 'True', 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'blogs.post': {
            'Meta': {'ordering': "[u'-date']", 'unique_together': "((u'slug', u'blog'),)", 'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.Blog']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.CharField', [], {'default': "u'rest'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'blogs.story': {
            'Meta': {'ordering': "[u'-date']", 'object_name': 'Story', '_ormbases': [u'blogs.Post']},
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['blogs.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fileshack.store': {
            'Meta': {'object_name': 'Store'},
            'accesscode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'allow_watch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'protect_files': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'store_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'watch_delay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '360'})
        }
    }

    complete_apps = ['blogs']