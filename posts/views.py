from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm
from .models import Group, Post, User


class Meta:
    ordering = Post.objects.order_by("-pub_date")


def get_paginated_view(request, post_list, page_size=10):
    paginator = Paginator(post_list, page_size)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    post_list = Meta.ordering.all()
    page, paginator = get_paginated_view(request, post_list)
    context = {"page": page, "paginator": paginator}
    return render(request, "index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by("-pub_date").all()
    page, paginator = get_paginated_view(request, post_list)
    context = {"group": group, "page": page, "paginator": paginator}
    return render(request, "group.html", context)


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect("index")

        return render(request, "new_post.html", {"form": form})

    form = PostForm()
    return render(request, "new_post.html", {"form": form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.order_by("-pub_date").all()
    page, paginator = get_paginated_view(request, post_list)
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

    post = get_object_or_404(user.posts.all(), pk=post_id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST":
        if form.is_valid():
            post.pub_date = timezone.now()
            form.save()
            return redirect("post_detail", username=username, post_id=post.pk)
        return render(request, "new_post.html", {"form": form, "post": post})
    return render(request, "new_post.html", {"form": form, "post": post})
