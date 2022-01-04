from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from user_profile.models import Profile

class ProfileSignupForm(SignupForm):
    accept_marketing_email = forms.BooleanField(
        label=_(
            "Allow sending of marketing and other communication via email"
        ),
        required=False,
    )

    def save(self, request):
        instance = super(ProfileSignupForm, self).save(request)
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.has_accepted_marketing = self.cleaned_data[
            "accept_marketing_email"
        ]
        profile.save()
        return instance
