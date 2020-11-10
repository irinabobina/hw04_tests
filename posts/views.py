from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {"page": page, "paginator": paginator}
    return render(request, "index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {"group": group, "page": page, "paginator": paginator}
    return render(request, "group.html", context)


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(request, "new_post.html", {"form": form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html",
                  {"page": page, "paginator": paginator, "author": author})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(author.posts.all(), pk=post_id)
    return render(request, "post.html", {"post": post, "author": author})


def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("post_detail", username=username, post_id=post_id)
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post_detail", username=username, post_id=post.pk)
    return render(request, "new_post.html", {"form": form, "post": post})
