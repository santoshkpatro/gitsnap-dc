from django.db import models

from gitsnap.common.models import BaseModel
from gitsnap.projects.models import Project
from gitsnap.users.models import User


class Issue(BaseModel):
    class State(models.TextChoices):
        Open = "open", "Open"
        Closed = "closed", "Closed"

    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="project_issues"
    )
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="author_issues", null=True
    )
    assignee = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="assignee_issues",
        blank=True,
        null=True,
    )
    number = models.IntegerField(blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=6, default=State.Open, choices=State.choices)

    class Meta:
        db_table = "issues"
        unique_together = ["project", "number"]

    def __str__(self) -> str:
        return self.title
