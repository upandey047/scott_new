from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "has_accepted_marketing")
    list_filter = ("has_accepted_marketing",)
    search_fields = ("user__email", "user__first_name", "user__last_name")
    raw_id_fields = ("user",)
