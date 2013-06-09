from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blogs.models import Blog, Post, Story
from blogs.forms import BlogForm, PostForm, StoryForm

from fileshack.models import Store
import fileshack.views

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class OwnerOnlyMixin(LoginRequiredMixin):

    def check_owner(self, request):
        self.object = self.get_object()
        return request.user==self.object.owner

    def get(self, request, *args, **kwargs):
        if not self.check_owner(request):
            raise PermissionDenied()
        return super(OwnerOnlyMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.check_owner(request):
            raise PermissionDenied()
        return super(OwnerOnlyMixin, self).post(request, *args, **kwargs)


# Blog CRUD

class BlogCreate(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(OwnerOnlyMixin, UpdateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

class BlogDelete(OwnerOnlyMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('profile')


# Post CRUD

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        context['blog'] = self.kwargs.get('blog_id', None)
        if not context['blog']:
            if self.request.user.owner_of.all():
                context['blog'] = self.request.user.owner_of.all()[0].id
        if not context['blog']:
            if self.request.user.member_of.all():
                context['blog'] = self.request.user.member_of.all()[0].id
        context['form'].fields['blog'].queryset = Blog.objects.filter(Q(owner=self.request.user)|Q(pk__in=self.request.user.member_of.all()))
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        blog = form.instance.blog
        if self.request.user != blog.owner and self.request.user not in blog.members.objects.all():
            raise forms.ValidationError("You can't post in that blog.")
        return super(PostCreate, self).form_valid(form)

class PostUpdate(OwnerOnlyMixin, UpdateView):

    def check_owner(self, request):
        self.object = self.get_object()
        return request.user==self.object.blog.owner or\
            request.user in self.object.blog.members.all()

    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

class PostDelete(OwnerOnlyMixin, DeleteView):

    def check_owner(self, request):
        self.object = self.get_object()
        return request.user==self.object.blog.owner or\
            request.user in self.object.blog.members.all()

    model = Post
    success_url = reverse_lazy('profile')

# Story CRUD

class StoryCreate(PostCreate):
    form_class = StoryForm
    model = Story
    template_name = "blogs/post_form.html"  # Until something different is done

class StoryUpdate(PostUpdate):
    form_class = StoryForm
    model = Story
    template_name = "blogs/post_form.html"  # Until something different is done

class StoryDelete(PostDelete):
    model = Story
    template_name = "blogs/post_form.html"  # Until something different is done


# Special View for the profile|home

class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "blogs/profile.html"

import nikola.plugins.compile_rest
import nikola.plugins.compile_markdown
import nikola.plugins.compile_textile

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def rest_preview(request):
    markup = nikola.plugins.compile_rest.rst2html(request.POST.get('data', ''))[0]
    return render_to_response( 'blogs/preview.html',
                              {'preview': markup},
                              context_instance=RequestContext(request))

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def markdown_preview(request):
    markup = nikola.plugins.compile_markdown.markdown(request.POST.get('data', ''))
    return render_to_response( 'blogs/preview.html',
                              {'preview': markup},
                              context_instance=RequestContext(request))

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def textile_preview(request):
    markup = nikola.plugins.compile_textile.textile(request.POST.get('data', ''))
    return render_to_response( 'blogs/preview.html',
                              {'preview': markup},
                              context_instance=RequestContext(request))


def require_store_access(view, makes_dirty = False):
    def view_wrapper(request, *args, **kwargs):
        if not kwargs.has_key("store_path"):
            raise Http404()
        store_path = kwargs["store_path"]
        if  len(store_path) > 0 and store_path[-1] == "/":
            store_path = store_path[:-1]
        store = get_object_or_404(fileshack.views.Store, path=store_path)
        blog_id = int(store.path.split('/')[0])
        blog = get_object_or_404(Blog, id=blog_id)
        if request.user == blog.owner or request.user in blog.members.all():
            if makes_dirty:
                blog.dirty = True
                blog.save()
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return view_wrapper

# Monkeypatch Fileshack views
fileshack.views.index = require_store_access(fileshack.views.index)
fileshack.views.iframe = require_store_access(fileshack.views.iframe)
fileshack.views.upload = require_store_access(fileshack.views.upload, True)
fileshack.views.delete = require_store_access(fileshack.views.delete, True)
fileshack.views.download = require_store_access(fileshack.views.download)
fileshack.views.update = require_store_access(fileshack.views.update, True)

# Store creation
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def store_create(request, parent_path):
    path = request.POST.get('path')
    if not path:
        raise PermissionDenied()
    a,b = parent_path.split('/')[:2]
    blog = get_object_or_404(Blog, id=int(a))
    if b not in ['galleries', 'files', 'listings']:
        raise PermissionDenied()
    if '/' in path:
        raise PermissionDenied()
    fullpath = '/'.join([parent_path, path]).replace('//', '/')
    new_store = Store(path=fullpath)
    new_store.save()
    blog.stores.add(new_store)
    blog.save()
    return redirect(reverse_lazy('profile')+"#tab4")

