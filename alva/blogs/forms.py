# forms.py
import datetime
import re

from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput
from datetimewidget.widgets import DateTimeWidget
from markitup.widgets import MarkItUpWidget

from blogs.models import Blog, Post, Story

NAME_REGEX = re.compile('^[a-zA-Z0-9]+$')

class NameWidget(BootstrapTextInput):
    def __init__(self, *a, **k):
        k['append'] = '.donewithniko.la'
        super(NameWidget, self).__init__(*a, **k)

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name', 'title', 'description', 'language')
        exclude = ('owner', 'dirty', 'members', 'domain')
        widgets = {
            'name': NameWidget,
            'description': forms.Textarea(attrs={'class': 'input-block-level'}),
            'title': BootstrapTextInput({'class': 'input-block-level'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if not NAME_REGEX.match(name):
            raise forms.ValidationError("Invalid characters")
        return name


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('blog', 'title', 'slug', 'tags', 'date', 'description', 'markup', 'text')
        exclude = ('author',)
        widgets = {
            'title': BootstrapTextInput({'class': 'input-block-level'}),
            'slug': BootstrapTextInput({'class': 'input-block-level'}),
            'tags': BootstrapTextInput({'class': 'input-block-level'}),
            'date': DateTimeWidget(),
            'description': forms.Textarea({'rows': 3, 'class': 'input-block-level'}),
            'text': forms.Textarea(),
        }

    def clean_dirty(self):
        # Basically, always dirty, to force blog sync
        return True

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author',)
