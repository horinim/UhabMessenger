from django.contrib import admin
from django.contrib.auth.models import User

from .models import (UsersList , GroupUser, Post, CommentPost, LikePost)

admin.site.register(UsersList)
admin.site.register(GroupUser)
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(LikePost)

