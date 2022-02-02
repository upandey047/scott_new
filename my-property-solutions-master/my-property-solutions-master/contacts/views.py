from django.shortcuts import render
from django.views.generic import TemplateView, View
from contacts.models import Contact
from contacts.forms import (
    CertifiersOrInspectorsForm,
    PropertiesInspectedFormSet,
    PropertiesInspectedModelFormSet,
    ConstructionOrTradeForm,
    PropertiesEmployedFormSet,
    PropertiesEmployedModelFormSet,
    DesignForm,
    DevelopersForm,
    FinanceForm,
    SurveyorsForm,
    LegalForm,
    RealEstateContactForm,
    CouncilContactForm,
    OthersForm,
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json


class ContactsView(LoginRequiredMixin, TemplateView):
    """
    This view shows the contacts i.e the agents and solicitors of a user.
    These contacts are fetched from the respective tables.
    """

    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-success", None):
            messages.success(
                self.request,
                "The Contact has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-success"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "contacts/contacts.html", ctx)

    def get_context_data(self, *args, **kwargs):
        contacts_sub_category = self.kwargs["contacts_sub_category"]
        contacts_category = self.kwargs["contacts_category"]
        print(self.kwargs["contacts_category"],self.kwargs["contacts_sub_category"])
        print(contacts_category)
        contacts = Contact.objects.filter(user=self.request.user).filter(
            sub_category=contacts_sub_category
        )
        ctx = {
            "contacts": contacts,
            "contacts_sub_category": contacts_sub_category,
            "contacts_category": contacts_category,
        }
        return ctx


class AddContactView(LoginRequiredMixin, View):
    template_name = "contacts/add_contact.html"
    contacts_category_form_map = {
        "certifiers-or-inspectors": CertifiersOrInspectorsForm,
        "construction-or-trade": ConstructionOrTradeForm,
        "design": DesignForm,
        "developers": DevelopersForm,
        "finance": FinanceForm,
        "surveyors": SurveyorsForm,
        "legal": LegalForm,
        "real-estate": RealEstateContactForm,
        "council": CouncilContactForm,
        "others": OthersForm,
    }

    def get_context_data(self, *args, **kwargs):
        # ctx = super(AddContactView, self).get_context_data(*args, **kwargs)
        ctx = {
            "contacts_category": self.kwargs["contacts_category"],
            "contacts_sub_category": self.kwargs["contacts_sub_category"],
        }
        form = self.contacts_category_form_map.get(
            self.kwargs["contacts_category"]
        )
        if form:
            ctx["form"] = form

        if self.kwargs["contacts_category"] == "certifiers-or-inspectors":
            ctx["properties_inspected_formset"] = PropertiesInspectedFormSet
        elif self.kwargs["contacts_category"] == "construction-or-trade":
            ctx["properties_employed_formset"] = PropertiesEmployedFormSet

        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "Contact created successfully",
            extra_tags="contact_created",
        )
        return reverse_lazy(
            "dashboard:contacts:index",
            kwargs={
                "contacts_category": self.kwargs["contacts_category"],
                "contacts_sub_category": self.kwargs["contacts_sub_category"],
            },
        )

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        formset = None
        if self.kwargs["contacts_category"] == "certifiers-or-inspectors":
            form = CertifiersOrInspectorsForm(request.POST)
            formset = PropertiesInspectedFormSet(request.POST)
        elif self.kwargs["contacts_category"] == "construction-or-trade":
            form = ConstructionOrTradeForm(request.POST)
            formset = PropertiesEmployedFormSet(request.POST)
        elif self.kwargs["contacts_category"] == "design":
            form = DesignForm(request.POST)
        elif self.kwargs["contacts_category"] == "developers":
            form = DevelopersForm(request.POST)
        elif self.kwargs["contacts_category"] == "finance":
            form = FinanceForm(request.POST)
        elif self.kwargs["contacts_category"] == "surveyors":
            form = SurveyorsForm(request.POST)
        elif self.kwargs["contacts_category"] == "legal":
            form = LegalForm(request.POST)
        elif self.kwargs["contacts_category"] == "real-estate":
            form = RealEstateContactForm(request.POST)
        elif self.kwargs["contacts_category"] == "council":
            form = CouncilContactForm(request.POST)
        elif self.kwargs["contacts_category"] == "others":
            form = OthersForm(request.POST)
        if formset:
            # This is for the two categories which consist of formsets.
            if form.is_valid() and formset.is_valid():
                return self.form_valid(form, formset)
            else:
                # Form or the formset is invalid
                return self.form_invalid(form, formset)
        else:
            # This is for all other categories where there is no formset
            if form.is_valid():
                return self.form_valid(form, formset)
            else:
                return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form_object = form.save(commit=False)
        form_object.user = self.request.user
        form_object.category = self.kwargs["contacts_category"]
        form_object.sub_category = self.kwargs["contacts_sub_category"]
        form_object.save()
        if formset:
            for formset_form in formset:
                if formset_form.has_changed():
                    form_obj = formset_form.save(commit=False)
                    form_obj.contact = form_object
                    form_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        ctx = {
            "contacts_category": self.kwargs["contacts_category"],
            "contacts_sub_category": self.kwargs["contacts_sub_category"],
            "form": form,
        }
        if formset:
            if self.kwargs["contacts_category"] == "certifiers-or-inspectors":
                ctx["properties_inspected_formset"] = formset
            elif self.kwargs["contacts_category"] == "construction-or-trade":
                ctx["properties_employed_formset"] = formset
        return render(self.request, self.template_name, ctx)


class EditContactView(LoginRequiredMixin, View):
    template_name = "contacts/edit_contact.html"

    def get_context_data(self, *args, **kwargs):
        ctx = {}
        contact_object = Contact.objects.get(pk=kwargs["contact_id"])
        properties_inspected = contact_object.propertiesinspected_set.all()
        properties_employed = contact_object.propertiesemployed_set.all()
        if self.kwargs["contacts_category"] == "certifiers-or-inspectors":
            ctx["form"] = CertifiersOrInspectorsForm(instance=contact_object)
            if properties_inspected:
                ctx[
                    "properties_inspected_formset"
                ] = PropertiesInspectedModelFormSet(
                    queryset=properties_inspected
                )
            else:
                ctx[
                    "properties_inspected_formset"
                ] = PropertiesInspectedFormSet()
        elif self.kwargs["contacts_category"] == "construction-or-trade":
            ctx["form"] = ConstructionOrTradeForm(instance=contact_object)
            if properties_employed:
                ctx[
                    "properties_employed_formset"
                ] = PropertiesEmployedModelFormSet(
                    queryset=properties_employed
                )
            else:
                ctx[
                    "properties_employed_formset"
                ] = PropertiesEmployedFormSet()
        elif self.kwargs["contacts_category"] == "design":
            ctx["form"] = DesignForm(instance=contact_object)
        elif self.kwargs["contacts_category"] == "developers":
            ctx["form"] = DevelopersForm(instance=contact_object)
        elif self.kwargs["contacts_category"] == "finance":
            ctx["form"] = FinanceForm(instance=contact_object)
        elif self.kwargs["contacts_category"] == "surveyors":
            ctx["form"] = SurveyorsForm(instance=contact_object)
        elif self.kwargs["contacts_category"] == "legal":
            ctx["form"] = LegalForm(instance=contact_object)
        elif (self.kwargs["contacts_category"] == "real-estate") or (
            self.kwargs["contacts_category"] == "real_estate"
        ):
            ctx["form"] = RealEstateContactForm(instance=contact_object)
        elif self.kwargs["contacts_category"] == "council":
            ctx["form"] = CouncilContactForm(instance=contact_object)
        elif self.kwargs["contacts_category"] == "others":
            ctx["form"] = OthersForm(instance=contact_object)
        ctx["contacts_category"] = self.kwargs["contacts_category"]
        ctx["contacts_sub_category"] = self.kwargs["contacts_sub_category"]
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "Contact updated successfully",
            extra_tags="contact_edited",
        )
        return reverse_lazy(
            "dashboard:contacts:index",
            kwargs={
                "contacts_category": self.kwargs["contacts_category"],
                "contacts_sub_category": self.kwargs["contacts_sub_category"],
            },
        )

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        contact_object = Contact.objects.get(pk=kwargs["contact_id"])
        properties_inspected = contact_object.propertiesinspected_set.all()
        formset = None
        if self.kwargs["contacts_category"] == "certifiers-or-inspectors":
            form = CertifiersOrInspectorsForm(
                request.POST, instance=contact_object
            )
            formset = PropertiesInspectedModelFormSet(
                request.POST, queryset=properties_inspected
            )
        elif self.kwargs["contacts_category"] == "construction-or-trade":
            form = ConstructionOrTradeForm(
                request.POST, instance=contact_object
            )
            formset = PropertiesEmployedModelFormSet(
                request.POST, queryset=properties_inspected
            )
        elif self.kwargs["contacts_category"] == "design":
            form = DesignForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "developers":
            form = DevelopersForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "finance":
            form = FinanceForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "surveyors":
            form = SurveyorsForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "legal":
            form = LegalForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "real-estate" or (
            self.kwargs["contacts_category"] == "real_estate"
        ):
            form = RealEstateContactForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "council":
            form = CouncilContactForm(request.POST, instance=contact_object)
        elif self.kwargs["contacts_category"] == "others":
            form = OthersForm(request.POST, instance=contact_object)
        if formset:
            # This is for the two categories which consist of formsets.
            if form.is_valid() and formset.is_valid():
                return self.form_valid(form, formset)
            else:
                # Form or the formset is invalid
                return self.form_invalid(form, formset)
        else:
            # This is for all other categories where there is no formset
            if form.is_valid():
                return self.form_valid(form, formset)
            else:
                return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form_object = form.save(commit=False)
        form_object.user = self.request.user
        form_object.category = self.kwargs["contacts_category"]
        form_object.sub_category = self.kwargs["contacts_sub_category"]
        form_object.save()
        if formset:
            for formset_form in formset:
                if formset_form.has_changed():
                    form_obj = formset_form.save(commit=False)
                    form_obj.contact = form_object
                    form_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        ctx = {
            "contacts_category": self.kwargs["contacts_category"],
            "contacts_sub_category": self.kwargs["contacts_sub_category"],
            "form": form,
        }
        if formset:
            if self.kwargs["contacts_category"] == "certifiers-or-inspectors":
                ctx["properties_inspected_formset"] = formset
            elif self.kwargs["contacts_category"] == "construction-or-trade":
                ctx["properties_employed_formset"] = formset
        return render(self.request, self.template_name, ctx)


class DeleteContactView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        contact_id = data["contact_id"]
        contact_obj = Contact.objects.get(pk=contact_id)
        contact_obj.delete()
        response = {"status": True}
        request.session["deletion-success"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )
