from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)