from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class NoteForMyself(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="note",null=True,blank=True,)
    note = models.CharField(_("Note"), max_length=500, null=True, blank=True)
