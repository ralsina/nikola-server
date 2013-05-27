# forms.py
import datetime

from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput
from datetimewidget.widgets import DateTimeWidget

from blogs.models import Blog, Post, Story


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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('blog', 'title', 'slug', 'tags', 'date', 'description', 'text')
        exclude = ('author',)
        widgets = {
            'title': BootstrapTextInput({'class': 'input-block-level'}),
            'slug': BootstrapTextInput({'class': 'input-block-level'}),
            'tags': BootstrapTextInput({'class': 'input-block-level'}),
            'date': DateTimeWidget(),
            'description': forms.Textarea({'rows': 3, 'class': 'input-block-level'}),
            'text': forms.Textarea({'rows': 25, 'class': 'input-block-level'}),
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author',)
