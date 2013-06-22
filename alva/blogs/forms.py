# forms.py
import datetime
import re

from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput
from datetimewidget.widgets import DateTimeWidget

from blogs.models import Blog, Post, Story
from nikola.utils import slugify

NAME_REGEX = re.compile('^[a-zA-Z0-9]+$')
TAG_REGEX = re.compile('^[a-zA-Z0-9 ,]*$')

class NameWidget(BootstrapTextInput):
    def __init__(self, *a, **k):
        k['append'] = '.donewithniko.la'
        super(NameWidget, self).__init__(*a, **k)

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name', 'title', 'description', 'language', 'theme', 'dirty')
        exclude = ('owner', 'members', 'domain')
        widgets = {
            'name': NameWidget,
            'description': forms.Textarea(attrs={'class': 'input-block-level'}),
            'title': BootstrapTextInput({'class': 'input-block-level'}),
            'dirty': forms.HiddenInput(),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if not NAME_REGEX.match(name):
            raise forms.ValidationError("Invalid characters.")
        if name in name in ['www', 'static', 'admin']:
            raise forms.ValidationError("That name is reserved.")
        return name

    def clean_markup(self):
        v = self.cleaned_data['markup']
        if not v in ('rest', 'markdown', 'textile'):
            raise forms.ValidationError("Invalid markup")

    def clean_dirty(self):
        # Basically, always dirty, to force blog sync
        self.cleaned_data['dirty'] = True
        return True


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('blog', 'title', 'slug', 'tags', 'date', 'description', 'markup', 'text', 'dirty')
        exclude = ('author',)
        widgets = {
            'title': BootstrapTextInput({'class': 'input-block-level'}),
            'slug': BootstrapTextInput({'class': 'input-block-level'}),
            'tags': BootstrapTextInput({'class': 'input-block-level'}),
            'date': DateTimeWidget(),
            'description': forms.Textarea({'rows': 3, 'class': 'input-block-level'}),
            'text': forms.Textarea(),
            'dirty': forms.HiddenInput(),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug != slugify(slug):
            raise forms.ValidationError("Just lowercase letters, numbers and '-' please.")
        return slug

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not TAG_REGEX.match(tags):
            raise forms.ValidationError("Just lowercase letters and numbers, separated by commas.")
        return tags

    def clean_dirty(self):
        # Basically, always dirty, to force blog sync
        self.cleaned_data['dirty'] = True
        return True

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author',)
