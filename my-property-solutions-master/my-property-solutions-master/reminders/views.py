from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Reminders
import datetime
from django.urls import reverse_lazy


class RemindersListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        reminders = Reminders.objects.filter(
            user=request.user, status__in=["pending", "snooze"]
        )
        reminders_queryset = reminders.filter(
            datetime__lte=datetime.datetime.now()
            + datetime.timedelta(hours=11)
        )
        return render(
            request,
            "reminders/reminders_notification.html",
            {"reminders": reminders_queryset},
        )


class DismissReminderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        reminder_obj = Reminders.objects.get(pk=kwargs["reminder_id"])
        reminder_obj.status = "complete"
        reminder_obj.save()
        return HttpResponseRedirect(
            reverse_lazy("dashboard:reminders:reminders_list")
        )


class SnoozeReminderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        reminder_obj = Reminders.objects.get(pk=kwargs["reminder_id"])
        reminder_obj.status = "snooze"
        datetime_obj = reminder_obj.datetime + datetime.timedelta(minutes=30)
        reminder_obj.datetime = datetime_obj
        reminder_obj.user = self.request.user
        reminder_obj.save()
        return HttpResponseRedirect(
            reverse_lazy("dashboard:reminders:reminders_list")
        )
