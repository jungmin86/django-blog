from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "blog/post_detail.html", {"post": post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", id=post.id)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form, "is_editing": False})


@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form, "is_editing": True})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
    return render(request, "blog/post_draft_list.html", {"posts": posts})


@login_required
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect("post_detail", id=id)


def post_remove(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("post_list")


def add_comment_to_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username
            comment.save()
            return redirect("post_detail", id=post.id)
    else:
        form = CommentForm()
    return render(request, "blog/add_comment_to_post.html", {"form": form})


@login_required
def comment_approve(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.approve()
    return redirect("post_detail", id=comment.post.id)


@login_required
def comment_remove(request, id):
    comment = get_object_or_404(Comment, pk=id)
    comment.delete()
    return redirect("post_detail", id=comment.post.id)
