from email.policy import default
from django.db import models


class Todo(models.Model):
    creation_date = models.DateTimeField(null=False)
    closing_date = models.DateTimeField(null=True)
    is_closed = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField()
