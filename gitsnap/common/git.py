import pygit2
from django.conf import settings

class Git:
    @classmethod
    def initiate_project(cls, name):
        path = settings.MEDIA_ROOT / f'{name}.git'
        pygit2.init_repository(path, bare=True)
        return path