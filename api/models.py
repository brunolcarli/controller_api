from email.policy import default
from django.db import models


class Todo(models.Model):
    creation_date = models.DateTimeField(null=False)
    closing_date = models.DateTimeField(null=True)
    is_closed = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField()
    task_id = models.CharField(max_length=500, blank=False, null=False)
    username = models.CharField(max_length=100, blank=False, null=False)
    reopen_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('username', 'task_id')
