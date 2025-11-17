from django.shortcuts import render
from django.db.models import Q


# Create your views here.
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Post, Comment, Like, Message, Profile


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect("feed")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def feed_view(request):
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("likes", "comments")
        .order_by("-created_at")
    )
    return render(request, "core/feed.html", {"posts": posts})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.order_by("-created_at")
    profile, _ = Profile.objects.get_or_create(user=user)
    return render(
        request,
        "core/profile.html",
        {"profile_user": user, "profile": profile, "posts": posts},
    )


@login_required
def create_post_view(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption", "")
        if image:
            Post.objects.create(author=request.user, image=image, caption=caption)
        return redirect("feed")
    return render(request, "core/create_post.html")


@login_required
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect("feed")


@login_required
@require_http_methods(["GET", "POST"])
def chat_view(request, username):
    other = get_object_or_404(User, username=username)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(sender=request.user, receiver=other, text=text)
        return HttpResponse(status=204)

    messages = Message.objects.filter(
        sender__in=[request.user, other], receiver__in=[request.user, other]
    )
    return render(request, "core/chat.html", {"other": other, "messages": messages})
@login_required
def conversations_view(request):
    # All messages involving the current user
    qs = (
        Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        )
        .select_related("sender", "receiver")
        .order_by("-created_at")
    )

    conversations = {}  # key: other_user_id -> data

    for m in qs:
        other = m.receiver if m.sender == request.user else m.sender
        data = conversations.get(other.id)
        if not data:
            conversations[other.id] = {
                "user": other,
                "last_message": m,
                "unread_count": 0,
            }
        # count unread messages where YOU are the receiver
        if not m.is_read and m.receiver == request.user:
            conversations[other.id]["unread_count"] += 1

    # Turn dict into a list (for the template)
    conversation_list = list(conversations.values())

    # Sort by latest message time (already mostly sorted, but just to be sure)
    conversation_list.sort(
        key=lambda c: c["last_message"].created_at, reverse=True
    )

    return render(
        request,
        "core/conversations.html",
        {"conversations": conversation_list},
    )
