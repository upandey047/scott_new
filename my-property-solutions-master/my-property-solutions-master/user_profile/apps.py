from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = "user_profile"

    def ready(self):
        import user_profile.signals  # NOQA F401
