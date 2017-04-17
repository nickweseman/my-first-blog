from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from blog.forms import CommentForm
from blog.forms import PostForm
from blog.models import Comment
from blog.models import Post


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by(
        'created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required()
def post_publish(request, pk):
    post = Post.objects.get(pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required()
def post_remove(request, pk):
    Post.objects.filter(pk=pk).delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required()
def comment_remove(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    comment.delete()
    return redirect('post_detail', pk=post.pk)


@login_required()
def comment_approve(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)



