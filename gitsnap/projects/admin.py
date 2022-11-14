from django.contrib import admin
from gitsnap.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'is_private']