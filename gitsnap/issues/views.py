from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError

from gitsnap.projects.models import Project
from gitsnap.users.models import User
from gitsnap.issues.models import Issue
from gitsnap.comments.models import Comment
from gitsnap.tags.models import Tag


class IssueListView(View):
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
        tags = request.GET.getlist("tags")
        state = request.GET.get("state", "open")
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        issues = Issue.objects.filter(project=project, state=state)
        if tags:
            issues = issues.filter(issue_tags__name__in=tags).distinct()

        available_tags = Tag.objects.filter(project=project, type=Tag.Type.Issue)
        open_issues_count = Issue.objects.filter(
            project=project, state=Issue.State.Open
        ).count()
        closed_issues_count = Issue.objects.filter(
            project=project, state=Issue.State.Closed
        ).count()

        context = {
            "username": username,
            "name": name,
            "tab": "issues",
            "issues": issues,
            "available_tags": available_tags,
            "added_tags": tags,
            "open_issues_count": open_issues_count,
            "closed_issues_count": closed_issues_count,
            "project": project,
        }

        return render(request, "issues/issue_list.html", context)


class IssueCreateView(LoginRequiredMixin, View):
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

        context = {
            "username": username,
            "name": name,
            "tab": "issues",
            "project": project,
        }

        return render(request, "issues/issue_create.html", context)

    def post(self, request, username, name):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        title = request.POST.get("title")
        description = request.POST.get("description", None)

        issue_number = 1
        last_issue = Issue.objects.filter(project=project).order_by("number").last()
        if last_issue:
            issue_number = last_issue.number + 1

        try:
            new_issue = Issue.objects.create(
                title=title,
                description=description,
                project=project,
                author=request.user,
                number=issue_number,
                state=Issue.State.Open,
            )

            return redirect(
                "issue-detail-view",
                username=username,
                name=name,
                number=new_issue.number,
            )
        except DatabaseError:
            raise Http404


class IssueDetailView(View):
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

    def get(self, request, username, name, number):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        try:
            issue = Issue.objects.get(project=project, number=number)
            comments = Comment.objects.filter(
                issue=issue, comment_type=Comment.CommentType.Issue
            )
        except Issue.DoesNotExist:
            raise Http404

        context = {
            "username": username,
            "name": name,
            "number": number,
            "tab": "issues",
            "issue": issue,
            "comments": comments,
            "project": project,
        }

        return render(request, "issues/issue_detail.html", context)


class IssueCommentCreateView(LoginRequiredMixin, View):
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

    def post(self, request, username, name, number):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        try:
            issue = Issue.objects.get(project=project, number=number)
            body = request.POST.get("body", None)

            if not issue:
                return HttpResponse(status=500)

            Comment.objects.create(
                author=request.user,
                issue=issue,
                comment_type=Comment.CommentType.Issue,
                body=body,
            )

            return redirect(
                "issue-detail-view", username=username, name=name, number=number
            )
        except Issue.DoesNotExist:
            raise Http404


class IssueCloseView(LoginRequiredMixin, View):
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

    def get(self, request, username, name, number):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        try:
            issue = Issue.objects.get(project=project, number=number)
            issue.state = Issue.State.Closed
            issue.save()

            return redirect(
                "issue-detail-view", username=username, name=name, number=number
            )
        except Issue.DoesNotExist:
            raise Http404


class IssueOpenView(LoginRequiredMixin, View):
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

    def get(self, request, username, name, number):
        project: Project = self.get_project(username, name)

        if not self.has_project_permission(request.user, project):
            raise Http404

        try:
            issue = Issue.objects.get(project=project, number=number)
            issue.state = Issue.State.Open
            issue.save()

            return redirect(
                "issue-detail-view", username=username, name=name, number=number
            )
        except Issue.DoesNotExist:
            raise Http404
