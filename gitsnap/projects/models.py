import uuid
import pygit2
from git import Repo
from django.db import models
from django.conf import settings
from django.utils.timezone import datetime, get_default_timezone

from gitsnap.common.models import BaseModel
from gitsnap.users.models import User


class Project(BaseModel):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        related_name='projects'
    )
    name = models.CharField(max_length=100)
    is_private = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    path = models.FileField(upload_to='projects/paths', blank=True, null=True)
    default_branch = models.CharField(max_length=100, default='main')

    class Meta:
        db_table = 'projects'
        unique_together = ['owner', 'name']

    def __str__(self) -> str:
        return self.name

    @classmethod
    def initiate_remote_repo(cls):
        root_url = str(settings.MEDIA_ROOT)
        path = f'projects/paths/{uuid.uuid4().hex}.git'
        pygit2.init_repository(root_url + '/' + path, bare=True)
        return path

    
    def get_repo_url(self):
        return self.path.path
    
    def get_repo(self) -> Repo:
        repo = Repo(self.get_repo_url())
        return repo

    def get_branches(self):
        repo = self.get_repo()
        branches = []
        for branch in repo.branches:
            branches.append(branch.name)
        return branches

    def get_project_tree(self, branch=None):
        repo = self.get_repo()
        if not branch:
            return repo.heads[self.default_branch].commit.tree
        
        return repo.heads[branch].commit.tree

    def get_root_tree_contents(self):
        root_tree = self.get_project_tree()
        contents = []
        for tree in root_tree.trees:
            contents.append({
                'name': tree.name,
                'type': 'folder'
            })

        for blob in root_tree.blobs:
            contents.append({
                'name': blob.name,
                'type': 'file',
            })
        return contents


    def get_tree_contents(self, branch, nested=None):
        tree = self.get_project_tree(branch)

        if nested:
            for dir in nested:
                for t in tree.trees:
                    if t.name == dir:
                        tree = t
                        break

        contents = []
        for t in tree.trees:
            contents.append({
                'name': t.name,
                'type': 'folder'
            })

        for b in tree.blobs:
            contents.append({
                'name': b.name,
                'type': 'file',
            })
        return contents


    def get_blob(self, branch, dir, file):
        tree = self.get_project_tree(branch)

        for folder in dir:
            for t in tree.trees:
                if t.name == folder:
                    tree = t
                    break
        
        blob = None
        for b in tree.blobs:
            if b.name == file:
                blob = b

        return blob


    def get_project_commits(self, branch='main'):
        commits = []
        repo = self.get_repo()

        for commit in repo.iter_commits(branch):
            commits.append(
                {
                    'message': commit.message,
                    'author': commit.author.name,
                    'committed_date': datetime.fromtimestamp(commit.committed_date, get_default_timezone()),
                    'hexsha': commit.hexsha
                }
            )
        return commits

    def get_commit_count(self, branch='main'):
        repo = self.get_repo()
        return len(list(repo.iter_commits(branch)))


    def get_readme_blob(self, tree):
        for blob in tree.blobs:
            if blob.name == 'README.md':
                return blob.data_stream.read()
        return None
        