from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Status, Comment
from .forms import CommentForm
from django.urls import reverse_lazy, reverse

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        filter_type = self.request.GET.get('filter', 'all')
        
        published_status, created = Status.objects.get_or_create(
            name='Published',
            defaults={'description': 'Posts available for all to view'}
        )
        draft_status, created = Status.objects.get_or_create(
            name='Draft',
            defaults={'description': 'Posts visible only to the author'}
        )
        archived_status, created = Status.objects.get_or_create(
            name='Archived',
            defaults={'description': 'Old posts visible only to logged-in users'}
        )
        
        if filter_type == 'my_posts' and self.request.user.is_authenticated:
            # Show only user's own PUBLISHED posts
            return Post.objects.filter(author=self.request.user, status=published_status).order_by('-created_on')
        
        elif filter_type == 'drafts' and self.request.user.is_authenticated:
            # Show only user's drafts
            return Post.objects.filter(author=self.request.user, status=draft_status).order_by('-created_on')
        
        elif filter_type == 'archived' and self.request.user.is_authenticated:
            # Show only user's archived posts
            return Post.objects.filter(author=self.request.user, status=archived_status).order_by('-created_on')
        
        else:
            # Default "All Posts": Show all published posts (everyone's) + mock posts if empty
            return Post.objects.filter(status=published_status).order_by('-created_on')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all comments for this post to context
        context['comments'] = self.object.comments.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Save comment with post and author
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'subtitle', 'body', 'image']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # Check which button was clicked
        if 'save_draft' in self.request.POST:
            draft_status, created = Status.objects.get_or_create(
                name='Draft',
                defaults={'description': 'Posts visible only to the author'}
            )
            form.instance.status = draft_status
        elif 'publish' in self.request.POST:
            published_status, created = Status.objects.get_or_create(
                name='Published',
                defaults={'description': 'Posts available for all to view'}
            )
            form.instance.status = published_status
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['title', 'subtitle', 'body', 'image']
    
    def test_func(self):
        # Check if logged-in user is the post author
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        # Check which button was clicked
        if 'archive_post' in self.request.POST:
            archived_status, created = Status.objects.get_or_create(
                name='Archived',
                defaults={'description': 'Old posts visible only to logged-in users'}
            )
            form.instance.status = archived_status
        elif 'unarchive_post' in self.request.POST:
            published_status, created = Status.objects.get_or_create(
                name='Published',
                defaults={'description': 'Posts available for all to view'}
            )
            form.instance.status = published_status
        elif 'save_draft' in self.request.POST:
            draft_status, created = Status.objects.get_or_create(
                name='Draft',
                defaults={'description': 'Posts visible only to the author'}
            )
            form.instance.status = draft_status
        elif 'publish' in self.request.POST:
            published_status, created = Status.objects.get_or_create(
                name='Published',
                defaults={'description': 'Posts available for all to view'}
            )
            form.instance.status = published_status
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('posts:list')
    
    def test_func(self):
        # Check if logged-in user is the post author
        post = self.get_object()
        return self.request.user == post.author


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'posts/comment_edit.html'
    
    def test_func(self):
        # Check if logged-in user is the comment author
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_delete.html'
    
    def test_func(self):
        # Check if logged-in user is the comment author
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.post.pk})