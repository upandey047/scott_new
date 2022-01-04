from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .models import Lead, Bank
from django.urls import reverse_lazy, reverse
from deals.models import Deal
from .forms import (
    LeadStatusForm,
    NewLeadForm,
    NewPropertyForm,
    NewPropertyOwnerForm,
)
from django.http import Http404


class IndexView(LoginRequiredMixin, TemplateView):
    """
    This view will be called when the user selects a category from the home page of the dashboard for viewing the leads of a particular category
    """

    template_name = "leads/index.html"

    def get_context_data(self, *args, **kwargs):
        """
        In the opening page of dashboard, various categories are displayed at the top.
        'category' will be used to highlight the selected button at the top
        """
        ctx = super(IndexView, self).get_context_data(**kwargs)
        category = self.request.path.rsplit("/", 1)[-1]
        if category not in [
            "bankruptcy",
            "deceased",
            "divorce",
            "liquidation",
            "mortgagee",
            "sheriff",
            "withdrawn",
            "sixty-days-over",
        ]:
            raise Http404
        lead_objects = Lead.objects.filter(
            category=category, user=self.request.user
        )
        ctx["category"] = category
        ctx["pending_leads"] = lead_objects.filter(status="pending")
        ctx["active_leads"] = lead_objects.filter(status="active")
        ctx["purchased_leads"] = lead_objects.filter(status="purchased")
        ctx["listed_leads"] = lead_objects.filter(status="listed")
        ctx["sold_leads"] = lead_objects.filter(status="sold")
        ctx["not_proceeding_leads"] = lead_objects.filter(
            status="not_proceeding"
        )
        return ctx


# The below templates will be used for the session wizard view defined below

TEMPLATES = {
    "0": "leads/add_lead_property_details.html",
    "1": "leads/add_lead_owner_details.html",
    "2": "leads/add_lead_agent_details.html",
    "3": "leads/add_lead_bank_details.html",
    "4": "leads/add_lead_solicitor_details.html",
}


class AddLeadWizard(LoginRequiredMixin, SessionWizardView):
    """
    This view will be called when the user would like to add a new category lead
    """

    template_name = "leads/add_lead_owner_details.html"

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        category = self.request.path.rsplit("/", 1)[-1]
        property_owner_object = (
            property_object
        ) = bank_object = real_estate_object = legal_object = None
        lead = Lead.objects.create(
            user=self.request.user, category=category, status="pending"
        )
        property_object = form_dict["0"].save(commit=False)
        property_object.lead = lead
        property_object.user = self.request.user
        property_object.save()
        # Saving the bank object no metter whether it is changed or not
        bank_object = form_dict["3"].save(commit=False)
        bank_object._property = property_object
        bank_object.save()
        if category == "deceased":
            for form in form_dict["2"]:
                real_estate_object = form.save(commit=False)
                real_estate_object.user = self.request.user
                real_estate_object._property = property_object
                real_estate_object.category = "real-estate"
                real_estate_object.sub_category = "executor"
                real_estate_object.save()
        else:
            real_estate_object = form_dict["2"].save(commit=False)
            real_estate_object.user = self.request.user
            real_estate_object._property = property_object
            real_estate_object.category = "real-estate"
            real_estate_object.sub_category = "agents"
            real_estate_object.save()
        if category == "divorce":
            for form in form_dict["4"]:
                legal_object = form.save(commit=False)
                legal_object.user = self.request.user
                legal_object._property = property_object
                legal_object.category = "legal"
                legal_object.sub_category = "conveyancers"
                legal_object.save()
        else:
            legal_object = form_dict["4"].save(commit=False)
            legal_object.user = self.request.user
            legal_object._property = property_object
            legal_object.category = "legal"
            legal_object.sub_category = "conveyancers"
            legal_object.save()
        # Create a deal object whenever a lead is created
        # Since there cna be multiple owners, a formset is used to save model form instances
        for form in form_dict["1"]:
            property_owner_object = form.save(commit=False)
            property_owner_object._property = property_object
            if category == "liquidation":
                property_owner_object.is_company = True
            property_owner_object.save()

        Deal.objects.create(lead=lead)
        return HttpResponseRedirect("/dashboard/leads/" + category)

    def get_context_data(self, *args, **kwargs):
        """
        In the opening page of dashboard, various categories are displayed at the top.
        'category' will be used to highlight the selected button at the top
        """
        category = self.request.path.rsplit("/", 1)[-1]
        if category not in [
            "bankruptcy",
            "deceased",
            "divorce",
            "liquidation",
            "mortgagee",
            "sheriff",
            "withdrawn",
            "sixty-days-over",
        ]:
            raise Http404
        ctx = super(AddLeadWizard, self).get_context_data(*args, **kwargs)
        ctx.update({"category": category})
        return ctx


class EditLeadStatus(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "leads/edit_lead_status.html", ctx)

    def get_context_data(self, *args, **kwargs):
        lead = Lead.objects.select_related("user", "property").get(
            pk=kwargs["lead_id"]
        )
        if lead.user != self.request.user:
            raise Http404
        ctx = {
            "property": lead.property,
            "form": LeadStatusForm(instance=lead),
            "category": lead.category,
        }
        return ctx

    def get_success_url(self, category):
        return reverse_lazy(
            "dashboard:leads:index", kwargs={"category": category}
        )

    def post(self, request, *args, **kwargs):
        lead = Lead.objects.select_related("user").get(pk=kwargs["lead_id"])
        if lead.user != self.request.user:
            raise Http404
        form = LeadStatusForm(request.POST, instance=lead)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        lead_obj = form.save(commit=False)
        lead_obj.user = self.request.user
        lead_obj.save()
        return HttpResponseRedirect(self.get_success_url(lead_obj.category))

    def form_invalid(self, form):
        lead = Lead.objects.select_related("property").get(
            pk=self.kwargs["lead_id"]
        )
        ctx = {
            "address": " ".join(
                [
                    str(element)
                    for element in [
                        lead.property.po_box,
                        lead.property.unit,
                        lead.property.number,
                        lead.property.street,
                        lead.property.suburb,
                        lead.property.state,
                        lead.property.post_code,
                    ]
                ]
            ),
            "form": form,
            "category": lead.category,
        }
        return render(self.request, "leads/edit_lead_status.html", ctx)


@login_required
def add_lead_view(request):
    if request.method == "POST":
        new_lead_form = NewLeadForm(request.POST)
        new_property_form = NewPropertyForm(request.POST)
        new_property_owner_form = NewPropertyOwnerForm(request.POST)

        if (
            new_lead_form.is_valid()
            and new_property_form.is_valid()
            and new_property_owner_form.is_valid()
        ):
            new_lead = new_lead_form.save(commit=False)
            new_lead.user = request.user
            new_lead.save()
            new_property = new_property_form.save(commit=False)
            new_property.lead = new_lead
            new_property.save()
            new_property_owner = new_property_owner_form.save(commit=False)
            new_property_owner._property = new_property
            new_property_owner.save()
            Deal.objects.get_or_create(lead=new_lead)
            Bank.objects.get_or_create(_property=new_property)
            return redirect(reverse("dashboard:index"))
    else:
        new_lead_form = NewLeadForm()
        new_property_form = NewPropertyForm()
        new_property_owner_form = NewPropertyOwnerForm()

    context = {
        "new_lead_form": new_lead_form,
        "new_property_form": new_property_form,
        "new_property_owner_form": new_property_owner_form,
    }
    return render(request, "leads/add_new_lead.html", context)
