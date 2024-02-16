from .base import TimeStampedModel
from django.db import models

class CrawlLink(TimeStampedModel):
    class Status(models.TextChoices):
        WAITING = 'waiting'
        COMPLETE = 'complete'
        FAILED = 'failed'
    link = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        null=True, blank=True
    )
    output_path = models.TextField(null=True, blank=True)
    download_at = models.DateTimeField(null=True, blank=True)
