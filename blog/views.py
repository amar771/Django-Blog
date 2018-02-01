from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .models import Post
from .models import Comment
from .models import Profile
from .forms import PostForm
from .forms import CommentForm
from .forms import ProfileForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).\
                                filter(is_active=True).\
                                order_by('-published_date')

    paginator = Paginator(posts, 25)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.first
        posts = paginator.page(1)

    except EmptyPage:
        # If page is out of range, deliver last page of results.page
        posts = paginator.page(paginator.num_pages)

    # return render(request, 'blog/post_list.html', {'posts': posts})
    return render(request, 'blog/index.html', {'posts': posts})


def index(request):
    return redirect('post_list')


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Checks if post is deleted and is user authenticated to view it
    if not post.is_active and not request.user.is_authenticated():
        return redirect('post_list')

    # Checks if post is published and is user authenticated to view it
    if not post.published_date and not request.user.is_authenticated():
        return redirect('post_list')

    return render(request, 'blog/post.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)

    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post,)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True)\
                        .order_by('created_date')

    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)

    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', slug=comment.post.slug)


@login_required
def comment_undelete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.undelete()
    return redirect('post_detail', slug=comment.post.slug)


@login_required
def deleted(request):
    posts = Post.objects.filter(is_active=False).order_by('created_date')
    return render(request, 'blog/deleted_posts.html', {'posts': posts})


def about_empty(request):
    return render(request, 'blog/about_empty.html')


def about(request):
    profile = Profile.objects.filter(pk=1)

    if not profile:
        return about_empty(request)

    return render(request, 'blog/about.html', {'profile': profile})


@login_required
def about_new(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('about')

        else:
            form = ProfileForm


@login_required
def about_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.post, instance=profile)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('about')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/about_edit.html', {'form': form})


def contact(request):
    return render(request, 'blog/contact.html')
