from django.db import DatabaseError, transaction
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View

from gitsnap.common.decorators import project_required
from gitsnap.projects.models import Project
from gitsnap.users.models import User
from gitsnap.issues.models import Issue


class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request, username):
        context = {"username": username}
        return render(request, "projects/project_create.html", context)

    def post(self, request, username):
        if not request.user.username == username:
            raise Http404

        # data = request.POST
        try:
            new_project = Project(
                name=request.POST.get("name"),
                description=request.POST.get("description", None),
                owner=request.user,
            )

            with transaction.atomic():
                path = Project.initiate_remote_repo()
                new_project.path.name = path
                new_project.save()

            return redirect(
                "project-detail-view",
                username=request.user.username,
                name=new_project.name,
            )
        except DatabaseError as e:
            print(e)
            return HttpResponse(status=500)


class ProjectDetailView(View):
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

    def get(self, request, username, name):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        if not project.check_empty_repo():
            context = {
                "project": project,
                "username": username,
                "name": project.name,
                "tab": "code",
            }
            return render(request, "projects/project_setup_guide.html", context)

        branches = project.get_branches()
        root_tree = project.get_project_tree()

        context = {
            "username": username,
            "name": name,
            "tab": "code",
            "contents": project.get_root_tree_contents(),
            "branches": branches,
            "total_branch": len(branches),
            "project": project,
            "commit_count": project.get_commit_count(project.default_branch),
            "last_commit": project.get_project_commits()[0],
            "readme_content": project.get_readme_blob(root_tree),
        }

        return render(request, "projects/project_detail.html", context)
