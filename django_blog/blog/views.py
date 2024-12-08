from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Comment
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Comment

@login_required
def CommentDeleteView(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        comment.delete()
        return redirect(comment.post.get_absolute_url())


@login_required
def CommentUpdateView(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def CommentCreateView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(post.get_absolute_url())


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        """Ensure only the author of the post can delete it."""
        return Post.objects.filter(author=self.request.user)
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Rest of the code  model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        """Ensure only the author of the post can edit it."""
        return Post.objects.filter(author=self.request.user)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect to the post list view after successful creation


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserCreationForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


# Use the default LoginView provided by Django


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
