from django.contrib import admin

from gitsnap.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment_type', 'author', 'issue', 'created_at']