from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
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
        Post.objects.select_related("user")
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
@login_required
def create_post_view(request):
    if request.method == "POST":
        media = request.FILES.get("media")          # <-- single field from template
        caption = request.POST.get("caption", "")

        post = Post(
            user=request.user,
            caption=caption,
        )

        if media:
            content_type = (media.content_type or "").lower()

            if content_type.startswith("image/"):
                post.image = media
            elif content_type.startswith("video/"):
                post.video = media

        post.save()
        return redirect("feed")

    return render(request, "core/create_post.html")


@login_required
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect("feed")


from django.contrib.auth.models import User
from django.db.models import Q

@login_required
@require_http_methods(["GET", "POST"])
def chat_view(request, username):
    other = get_object_or_404(User, username=username)

    # Handle new message POST (store in DB)
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(sender=request.user, receiver=other, text=text)
        return HttpResponse(status=204)

    # All messages between current user and "other"
    messages = Message.objects.filter(
        sender__in=[request.user, other],
        receiver__in=[request.user, other],
    ).order_by("created_at")

    # ✅ All users except yourself (no conversations filtering)
    all_users = User.objects.exclude(id=request.user.id).order_by("username")

    return render(
        request,
        "core/chat.html",
        {
            "other": other,
            "messages": messages,
            "all_users": all_users,
        },
    )



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# (these imports you already have, just make sure they exist)

@login_required
def edit_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        avatar = request.FILES.get("avatar")
        banner = request.FILES.get("banner")
        bio = request.POST.get("bio", "")

        if avatar:
            profile.avatar = avatar
        if banner:
            profile.banner = banner
        profile.bio = bio
        profile.save()
        return redirect("profile", username=request.user.username)

    return render(request, "core/edit_profile.html", {"profile": profile})

@login_required
def users_list_api(request):
    users = User.objects.all()
    data = []

    for u in users:
        profile, _ = Profile.objects.get_or_create(user=u)
        avatar_url = profile.avatar.url if profile.avatar else ""
        data.append(
            {
                "id": u.id,
                "username": u.username,
                "avatar_url": avatar_url,
            }
        )

    return JsonResponse({"users": data})
@login_required
def conversations_view(request):
    all_users = User.objects.exclude(id=request.user.id).order_by("username")

    return render(
        request,
        "core/conversations.html",
        {"all_users": all_users},
    )
