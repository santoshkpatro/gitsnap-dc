from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views import View

from gitsnap.projects.models import Project
from gitsnap.users.models import User


class CommitListView(View):
    def get_project(self, username, name):
        try:
            project = Project.objects.get(owner__username=username, name=name)

            return project
        except Project.DoesNotExist:
            raise Http404

    def has_project_permission(self, user: User, project: Project):
        if not project.is_private:
            return True
        
        if project.owner == user:
            return True

        return False

    def get(self, request, username, name, branch):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        commits = project.get_project_commits(branch)
        branches = project.get_branches()

        context = {
            'username': username,
            'name': name,
            'tab': 'commits',
            'project': project,
            'commits': commits,
            'branch': branch,
            'branches': branches
        }

        return render(request, 'commits/commit_list.html', context)
