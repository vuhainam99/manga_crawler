from .base import TimeStampedModel
from django.db import models

class IPRestriction(TimeStampedModel):
    class RestrictionType(models.TextChoices):
        MATCH = 'match'
    ip_or_domain = models.CharField(max_length=20, null=True, blank=True, default='127.0.0.1')
    type = models.CharField(
        max_length=10,
        choices=RestrictionType.choices,
        default=RestrictionType.MATCH,
        null=False, blank=False)
    title = models.TextField(null=True)