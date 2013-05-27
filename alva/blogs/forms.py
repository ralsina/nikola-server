# forms.py
from django import forms

from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapDateInput

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
        exclude = ('author', 'blogs')

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author',)
