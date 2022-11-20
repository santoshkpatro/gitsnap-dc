from django.db import models

from gitsnap.common.models import BaseModel
from gitsnap.issues.models import Issue
from gitsnap.users.models import User


class Comment(BaseModel):
    class CommentType(models.TextChoices):
        Issue = "issue", "Issue"
        MergeRequest = "merge_request", "Merge Request"

    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="issue_comments",
        blank=True,
        null=True,
    )
    # merge_request = models.ForeignKey(
    #     to=MergeRequest, on_delete=models.CASCADE,
    #     related_name='merge_request_comments',
    #     blank=True, null=True
    # )
    comment_type = models.CharField(max_length=15, choices=CommentType.choices)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="author_comments"
    )
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.body
