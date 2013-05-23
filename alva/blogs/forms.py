# forms.py
from django import forms
from blogs.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('owner', 'dirty', 'members')
