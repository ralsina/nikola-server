# forms.py
from django import forms
from blogs.models import Blog, Post, Story

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('owner', 'dirty', 'members')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author',)
