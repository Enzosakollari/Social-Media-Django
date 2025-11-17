from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # ROOT: ALWAYS SHOW LOGIN TEMPLATE
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
        ),
        name="login",
    ),

    # OPTIONAL: /login/ alias (same view, different URL, no redirect)
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
        ),
        name="login_alias",
    ),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", core_views.register_view, name="register"),

    # Main app
    path("feed/", core_views.feed_view, name="feed"),
    path("conversations/", core_views.conversations_view, name="conversations"),
    path("profile/<str:username>/", core_views.profile_view, name="profile"),
    path("post/new/", core_views.create_post_view, name="create_post"),
    path("post/<int:post_id>/like/", core_views.toggle_like_view, name="toggle_like"),
    path("chat/<str:username>/", core_views.chat_view, name="chat"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
