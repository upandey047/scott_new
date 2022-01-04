from django.urls import path
from django.conf.urls import include
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("leads/", include("leads.urls", namespace="leads")),
    path("contacts/", include("contacts.urls", namespace="contacts")),
    path("settings/", include("settings.urls", namespace="settings")),
    path("deals/", include("deals.urls", namespace="deals")),
    path("reminders/", include("reminders.urls", namespace="reminders")),
]
