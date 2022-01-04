from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from deals.models import Deal


class Reminders(models.Model):
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("complete", "complete"),
        ("snooze", "snooze"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, null=True, blank=True
    )
    notes = models.CharField(_("Notes"), max_length=300, null=True, blank=True)
    status = models.CharField(
        _("Status"), choices=STATUS_CHOICES, max_length=50, default="pending"
    )
    datetime = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(
        _("Created At"), auto_now_add=True, null=True, blank=True
    )
    dismissed_at = models.DateTimeField(
        _("Dismissed At"), null=True, blank=True
    )
    snooze = models.DateTimeField(_("Snooze"), null=True, blank=True)
