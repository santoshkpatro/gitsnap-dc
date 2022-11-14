from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views import View

from gitsnap.projects.models import Project
from gitsnap.users.models import User


class TreeView(View):
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

    def get(self, request, username, name, branch, path=''):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        contents = project.get_tree_contents(branch, nested=path.split('/'))
        branches = project.get_branches()
        commit_count = project.get_commit_count(branch)
        last_commit = project.get_project_commits(branch)[0]

        context = {
            'username': username,
            'name': name,
            'tab': 'code',
            'project': project,
            'contents': contents,
            'branch': branch,
            'branches': branches,
            'commit_count': commit_count,
            'last_commit': last_commit,
            'path': path
        }

        return render(request, 'tree/tree.html', context)
