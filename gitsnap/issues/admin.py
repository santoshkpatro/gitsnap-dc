from django.contrib import admin

from gitsnap.issues.models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['project', 'number', 'title', 'author']
