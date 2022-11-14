from django.shortcuts import redirect

from gitsnap.users.models import User
from gitsnap.projects.models import Project


def project_required(func):
    def wrap(request, *args, **kwargs):
        try:
            project: Project = Project.objects.get(
                owner__username=kwargs.get('username'),
                name=kwargs.get('name')
            )

            if project.is_private:
                if project.owner == request.user:
                    return redirect('index-view')  

            kwargs['project'] = project

            return func(request, *args, **kwargs)
        except Project.DoesNotExist:
            return redirect('index-view')

    return wrap