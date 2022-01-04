from django.urls import path
from . import views

app_name = "reminders"

urlpatterns = [
    path(
        "reminders-list",
        views.RemindersListView.as_view(),
        name="reminders_list",
    ),
    path(
        "dismiss-reminder/<int:reminder_id>",
        views.DismissReminderView.as_view(),
        name="dismiss_reminder",
    ),
    path(
        "snooze-reminder/<int:reminder_id>",
        views.SnoozeReminderView.as_view(),
        name="snooze_reminder",
    ),
]
