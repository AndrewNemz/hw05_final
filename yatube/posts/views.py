from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Follow
from .utils import paginator
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


PAGE_UPDATE: int = 20


@cache_page(PAGE_UPDATE)
def index(request):
    post_list = Post.objects.all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginator(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    user_posts = profile.posts.filter(author=profile).all()
    page_obj = paginator(request, user_posts)
    following = request.user.is_authenticated
    if following:
        following = profile.following.filter(user=request.user).exists()
    context = {
        'profile': profile,
        'page_obj': page_obj,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_post = post.author.posts.count()
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'post': post,
        'author_post': author_post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            form.save(commit=False).author = request.user
            form.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator(request, posts_list)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    if request.user != profile_user:
        Follow.objects.get_or_create(
            user=request.user, author=profile_user
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    profile_user = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=profile_user).delete()
    return redirect('posts:profile', username=username)
