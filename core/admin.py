from django.contrib import admin

from django.contrib import admin
from .models import Profile, Post, Comment, Like, Message

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Message)

# Register your models here.
