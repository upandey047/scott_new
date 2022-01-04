from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class Profile(models.Model):
    class Meta:
        app_label = "user_profile"
        db_table = "profile_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_accepted_marketing = models.BooleanField(
        _("Allow sending of marketing and other communication via email"),
        default=False,
    )
