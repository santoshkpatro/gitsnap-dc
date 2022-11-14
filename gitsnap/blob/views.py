from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views import View

from gitsnap.projects.models import Project
from gitsnap.users.models import User


class BlobView(View):
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

        branches = project.get_branches()
        # contents = project.get_tree_contents(branch, nested=path.split('/'))
        # commit_count = project.get_commit_count(branch)
        # last_commit = project.get_project_commits(branch)[0]

        dir = path.split('/')
        file = dir.pop()

        blob = project.get_blob(branch, dir, file)
        content = blob.data_stream.read().decode()
        size = blob.size
        file_name = blob.name

        context = {
            'username': username,
            'name': name,
            'tab': 'code',
            'project': project,
            'branch': branch,
            'branches': branches,
            'content': content,
            'path': path,
            'size': size,
            'file_name': file_name
        }

        return render(request, 'blob/blob.html', context)
