from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from leads.models import Lead
from .forms import NoteForMyselfForm
from django.urls import reverse_lazy


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "dashboard/index.html", ctx)

    def get_context_data(self, *args, **kwargs):
        """
        In the opening page of dashboard, various categories are displayed at the top.
        'category' will be used to highlight the selected button at the top
        """
        return {
            "form": NoteForMyselfForm(instance=self.request.user.note.first()),
            "leads": Lead.objects.filter(
                user=self.request.user, is_active=True, property__isnull=False
            ).select_related("property"),
        }

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully",
            extra_tags="submitted",
        )
        return reverse_lazy("dashboard:index")

    def post(self, request, *args, **kwargs):
        first_note = self.request.user.note.all().first()
        if first_note is not None:
            form = NoteForMyselfForm(request.POST, instance=first_note)
        else:
            form = NoteForMyselfForm(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        note_object = form.save(commit=False)
        note_object.user = self.request.user
        note_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        ctx = {"form": form}
        return render(self.request, "dashboard/index.html", ctx)
