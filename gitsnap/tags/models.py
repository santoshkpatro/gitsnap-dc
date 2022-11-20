from django.db import models
from gitsnap.common.models import BaseModel
from gitsnap.projects.models import Project
from gitsnap.issues.models import Issue


class Tag(BaseModel):
    class Type(models.TextChoices):
        Issue = "issue", "Issue"
        MergeRequest = "merge_request", "Merge Request"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tags")
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="issue_tags",
        blank=True,
        null=True,
    )
    # merge_request = models.ForeignKey(
    #     to=MergeRequest, on_delete=models.CASCADE,
    #     related_name='merge_request_tags',
    #     blank=True, null=True
    # )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=Type.choices)

    class Meta:
        db_table = "tags"
        unique_together = ["project", "name", "type"]

    def __str__(self) -> str:
        return self.name
