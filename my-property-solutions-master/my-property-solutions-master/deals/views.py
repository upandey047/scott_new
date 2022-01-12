from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    DealOverviewForm,
    PurchaseForm,
    HoldingCostsFormset,
    PurchaseComparableSalesForm,
    SaleForm,
    ProfitSplitFormset,
    ProfitSplitModelFormset,
    PurchaseComparableSalesImagesFormset,
    PurchaseComparableSalesImagesModelFormset,
    SaleComparableSalesForm,
    SaleComparableSalesImagesFormset,
    SaleComparableSalesImagesModelFormset,
    RenovationForm,
    SearchContactForm,
    RoomsDetailsForm,
    RoomsForm,
    ImagesFormset,
    ImagesModelFormset,
    ImagesForm,
    TasksFormset,
    TasksModelFormset,
    MyPurchaseDetailsForm,
    MyBankDetailsForm,
    MaterialsFormset,
    MaterialsModelFormset,
    PrimeCostItemsFormset,
    PurchaseCorrespondanceDocumentsFormset,
    PurchaseCorrespondanceDocumentsModelFormset,
    PurchaseCorrespondanceDocumentsForm,
    ExternalForm,
    ExternalLocationFormset,
    ExternalLocationModelFormset,
    ExternalDetailsForm,
    ExternalTasksFormset,
    ExternalTasksModelFormset,
    ExternalMaterialsFormset,
    ExternalMaterialsModelFormset,
    ExternalTasksForMyselfFormset,
    ExternalTasksForMyselfModelFormset,
    InternalTasksForMyselfFormset,
    InternalTasksForMyselfModelFormset,
    PurchaseCostsFormset,
    PurchaseFeasibilityReportForm,
    AFCAComplaintLodgedForm,
    ListForSaleForm,
    SoldForm,
    SaleDealInformationForm,
)
from .models import (
    Deal,
    PurchaseComparableSales,
    SaleComparableSales,
    Renovation,
    Team,
    Rooms,
    Tasks,
    Images,
    Materials,
    PrimeCostItems,
    PurchaseCorrespondanceDocuments,
    External,
    ExternalTasks,
    ExternalMaterials,
    AFCAComplaintLodged,
    ListForSale,
    Sold,
    SaleDealInformation,
)
from leads.models import Entry, Lounge, Dining, Bathroom, Bedroom
from leads.forms import (
    PropertyOwnerModelFormset,
    BankruptcyPropertyOwnerModelFormset,
    BankForm,
    LandDetailsForm,
    ZoningForm,
    ShapeForm,
    PropertyAddressForm,
    StreetAppealForm,
    ConstructionForm,
    ParkingForm,
    FeaturesForm,
    GrannyFlatForm,
    EntryModelFormset,
    LoungeModelFormset,
    DiningModelFormset,
    KitchenForm,
    LaundryForm,
    BathroomModelFormset,
    BedroomModelFormset,
    PersonalLoanFormset,
    TitleFormset,
    DealingFormset,
    PersonalLoanModelFormset,
    TitleModelFormset,
    DealingModelFormset,
    EntryForm,
    LoungeForm,
    DiningForm,
    BedroomForm,
    BathroomForm,
    AdditionalPropertyDetailsForm,
    AuctionForm,
    NotSheriffAuctionForm,
    LeadStatusForm,
)
from django.urls import reverse_lazy
from settings.models import CheckList, Entity
from settings.forms import CheckListFormSet
from contacts.forms import (
    RealEstateWithoutMarketForm,
    SolicitorModelFormSet,
    RealEstateModelFormset,
    PrivateLenderForm,
)
from contacts.models import Contact
from django.contrib import messages
import json
from reminders.models import Reminders
from reminders.forms import ReminderForm
from datetime import datetime
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class DealCardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/deal.html", ctx)

    @staticmethod
    def _get_auction_form(category):
        if category == "sheriff":
            return AuctionForm
        return NotSheriffAuctionForm

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead__property").get(
            lead_id=kwargs["lead_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        lead = deal.lead
        property_obj = deal.lead.property
        category = deal.lead.category
        sale_deal_info = SaleDealInformation.objects.filter(deal=deal)
        return {
            "lead_status_form": LeadStatusForm(instance=lead, prefix="lead"),
            "form": DealOverviewForm(instance=deal, prefix="purchase_deal"),
            "additional_property_details_form": AdditionalPropertyDetailsForm(
                instance=property_obj
            ),
            "auction_form": self._get_auction_form(category)(
                instance=property_obj.property_auction.all().first()
            ),
            "sale_deal_info_form": SaleDealInformationForm(
                instance=sale_deal_info.first(), prefix="sale_deal"
            ),
            "category": category,
            "lead_id": kwargs["lead_id"],
            "deal_id": deal.pk,
        }

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:deal", kwargs={"lead_id": self.kwargs["lead_id"]}
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead__property").get(
            lead_id=kwargs["lead_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        property_obj = deal.lead.property
        sale_deal_info = SaleDealInformation.objects.filter(deal=deal)
        form = DealOverviewForm(
            request.POST, instance=deal, prefix="purchase_deal"
        )
        category = deal.lead.category
        if sale_deal_info:
            sale_deal_info_form = SaleDealInformationForm(
                request.POST,
                instance=sale_deal_info.first(),
                prefix="sale_deal",
            )
        else:
            sale_deal_info_form = SaleDealInformationForm(
                request.POST, prefix="sale_deal"
            )
        if category == "withdrawn" or category == "sixty-days-over":
            second_form = AdditionalPropertyDetailsForm(
                request.POST, instance=property_obj
            )
        elif category == "sheriff":
            second_form = AuctionForm(
                request.POST,
                instance=property_obj.property_auction.all().first(),
            )
        else:
            second_form = NotSheriffAuctionForm(
                request.POST,
                instance=property_obj.property_auction.all().first(),
            )
        lead_status_form = LeadStatusForm(
            request.POST, instance=deal.lead, prefix="lead"
        )
        if (
            form.is_valid()
            and second_form.is_valid()
            and sale_deal_info_form.is_valid()
            and lead_status_form.is_valid()
        ):
            return self.form_valid(
                form,
                sale_deal_info_form,
                category,
                lead_status_form,
                second_form,
            )
        else:
            return self.form_invalid(
                form,
                sale_deal_info_form,
                deal,
                category,
                second_form,
                **kwargs
            )

    def form_valid(
        self,
        form,
        sale_deal_info_form,
        category,
        lead_status_form,
        second_form=None,
    ):
        deal_obj = form.save()
        lead_status_form.save()
        if sale_deal_info_form.has_changed():
            sale_deal_info = sale_deal_info_form.save(commit=False)
            sale_deal_info.deal = deal_obj
            sale_deal_info.save()
        if category == "withdrawn" or category == "sixty-days-over":
            if second_form:
                property_obj = second_form.save(commit=False)
                property_obj.lead = deal_obj.lead
                property_obj.save()
        else:
            if second_form:
                auction_obj = second_form.save(commit=False)
                auction_obj._property = deal_obj.lead.property
                auction_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self,
        form,
        sale_deal_info_form,
        deal,
        category,
        second_form=None,
        **kwargs
    ):
        ctx = {
            "form": form,
            "sale_deal_info_form": sale_deal_info_form,
            "lead_id": self.kwargs["lead_id"],
            "deal_id": deal.id,
            "category": deal.lead.category,
        }
        if category == "withdrawn" or category == "sixty-days-over":
            ctx["additional_property_details_form"] = second_form
        else:
            ctx["auction_form"] = second_form
        return render(self.request, "deals/deal.html", ctx)
    
class DealSaleCardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/dealsale.html", ctx)

    @staticmethod
    def _get_auction_form(category):
        if category == "sheriff":
            return AuctionForm
        return NotSheriffAuctionForm

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead__property").get(
            lead_id=kwargs["lead_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        lead = deal.lead
        property_obj = deal.lead.property
        category = deal.lead.category
        sale_deal_info = SaleDealInformation.objects.filter(deal=deal)
        return {
            "lead_status_form": LeadStatusForm(instance=lead, prefix="lead"),
            "form": DealOverviewForm(instance=deal, prefix="purchase_deal"),
            "additional_property_details_form": AdditionalPropertyDetailsForm(
                instance=property_obj
            ),
            "auction_form": self._get_auction_form(category)(
                instance=property_obj.property_auction.all().first()
            ),
            "sale_deal_info_form": SaleDealInformationForm(
                instance=sale_deal_info.first(), prefix="sale_deal"
            ),
            "category": category,
            "lead_id": kwargs["lead_id"],
            "deal_id": deal.pk,
        }

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:deal", kwargs={"lead_id": self.kwargs["lead_id"]}
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead__property").get(
            lead_id=kwargs["lead_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        property_obj = deal.lead.property
        sale_deal_info = SaleDealInformation.objects.filter(deal=deal)
        form = DealOverviewForm(
            request.POST, instance=deal, prefix="purchase_deal"
        )
        category = deal.lead.category
        if sale_deal_info:
            sale_deal_info_form = SaleDealInformationForm(
                request.POST,
                instance=sale_deal_info.first(),
                prefix="sale_deal",
            )
        else:
            sale_deal_info_form = SaleDealInformationForm(
                request.POST, prefix="sale_deal"
            )
        if category == "withdrawn" or category == "sixty-days-over":
            second_form = AdditionalPropertyDetailsForm(
                request.POST, instance=property_obj
            )
        elif category == "sheriff":
            second_form = AuctionForm(
                request.POST,
                instance=property_obj.property_auction.all().first(),
            )
        else:
            second_form = NotSheriffAuctionForm(
                request.POST,
                instance=property_obj.property_auction.all().first(),
            )
        lead_status_form = LeadStatusForm(
            request.POST, instance=deal.lead, prefix="lead"
        )
        if (
            form.is_valid()
            and second_form.is_valid()
            and sale_deal_info_form.is_valid()
            and lead_status_form.is_valid()
        ):
            return self.form_valid(
                form,
                sale_deal_info_form,
                category,
                lead_status_form,
                second_form,
            )
        else:
            return self.form_invalid(
                form,
                sale_deal_info_form,
                deal,
                category,
                second_form,
                **kwargs
            )

    def form_valid(
        self,
        form,
        sale_deal_info_form,
        category,
        lead_status_form,
        second_form=None,
    ):
        deal_obj = form.save()
        lead_status_form.save()
        if sale_deal_info_form.has_changed():
            sale_deal_info = sale_deal_info_form.save(commit=False)
            sale_deal_info.deal = deal_obj
            sale_deal_info.save()
        if category == "withdrawn" or category == "sixty-days-over":
            if second_form:
                property_obj = second_form.save(commit=False)
                property_obj.lead = deal_obj.lead
                property_obj.save()
        else:
            if second_form:
                auction_obj = second_form.save(commit=False)
                auction_obj._property = deal_obj.lead.property
                auction_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self,
        form,
        sale_deal_info_form,
        deal,
        category,
        second_form=None,
        **kwargs
    ):
        ctx = {
            "form": form,
            "sale_deal_info_form": sale_deal_info_form,
            "lead_id": self.kwargs["lead_id"],
            "deal_id": deal.id,
            "category": deal.lead.category,
        }
        if category == "withdrawn" or category == "sixty-days-over":
            ctx["additional_property_details_form"] = second_form
        else:
            ctx["auction_form"] = second_form
        return render(self.request, "deals/dealsale.html", ctx)


class CheckListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/checklist.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404

        if kwargs["category"] not in [
            "initial_research",
            "letters",
            "inspection",
            "due_diligence",
            "property_searches",
            "offer_or_finance",
            "renovation",
            "market_research",
            "exchange_or_settlement",
            "listing_for_sale",
            "sale-exchange_or_settlement",
        ]:
            raise Http404

        checklist_queryset = CheckList.objects.filter(
            deal_id=kwargs["deal_id"],
            user=self.request.user,
            category__category_name=kwargs["category"],
        )
        checklist_formset = CheckListFormSet(queryset=checklist_queryset)
        lead_id = deal.lead.id
        ctx = {
            "formset": checklist_formset,
            "category": kwargs["category"],
            "lead_id": lead_id,
            "deal_id": kwargs["deal_id"],
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:checklist",
            kwargs={
                "deal_id": self.kwargs["deal_id"],
                "category": self.kwargs["category"],
            },
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        checklist_queryset = CheckList.objects.filter(
            deal_id=kwargs["deal_id"],
            user=self.request.user,
            category__category_name=kwargs["category"],
        )
        checklist_formset = CheckListFormSet(
            request.POST, queryset=checklist_queryset
        )
        if checklist_formset.is_valid():
            return self.form_valid(checklist_formset)
        else:
            return self.form_invalid(checklist_formset)

    def form_valid(self, checklist_formset):
        for form in checklist_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, checklist_formset):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_id = deal.lead.id
        ctx = {
            "formset": checklist_formset,
            "category": self.kwargs["category"],
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_id,
        }
        return render(self.request, "deals/checklist.html", ctx)


class OwnerDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/owner_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        agent_object = None
        deal_object = Deal.objects.select_related("lead__property__bank").get(
            pk=kwargs["deal_id"]
        )
        if deal_object.lead.user != self.request.user:
            raise Http404
        property_obj = deal_object.lead.property
        category = deal_object.lead.category
        if category == "deceased":
            executor_object = property_obj.contact_set.all().filter(
                category="real-estate", sub_category="executor"
            )
            agent_object = (
                property_obj.contact_set.all()
                .filter(category="real-estate", sub_category="agents")
                .first()
            )
            if not agent_object:
                agent_object = Contact.objects.create(
                    user=self.request.user,
                    _property=property_obj,
                    category="real-estate",
                    sub_category="agents",
                )
        else:
            executor_object = (
                property_obj.contact_set.all()
                .filter(category="real-estate", sub_category="agents")
                .first()
            )
        solicitor_queryset = property_obj.contact_set.all().filter(
            category="legal"
        )
        bank_object = property_obj.bank
        ctx = {
            "lead_id": deal_object.lead.id,
            "deal_id": kwargs["deal_id"],
            "deal": deal_object,
            "executor_obj": executor_object,
            "solicitor": solicitor_queryset,
            "bank": bank_object,
            "category": category,
            "agent_obj": agent_object,
        }
        return ctx


class EditOwnerDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/owner/edit_owner_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead__property").get(
            pk=kwargs["deal_id"]
        )
        if deal_object.lead.user != self.request.user:
            raise Http404
        lead_object = deal_object.lead
        property_owner_queryset = lead_object.property.property_owner.all()
        ctx = {"deal_id": kwargs["deal_id"], "category": lead_object.category}
        if lead_object.category == "liquidation":
            ctx["formset"] = BankruptcyPropertyOwnerModelFormset(
                queryset=property_owner_queryset
            )
        else:
            ctx["formset"] = PropertyOwnerModelFormset(
                queryset=property_owner_queryset
            )
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The owner details have been saved successfully",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:owner_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead").get(
            pk=kwargs["deal_id"]
        )
        if deal_object.lead.user != self.request.user:
            raise Http404
        lead_object = deal_object.lead
        property_owner_queryset = lead_object.property.property_owner.all()
        if lead_object.category == "liquidation":
            formset = BankruptcyPropertyOwnerModelFormset(
                request.POST, queryset=property_owner_queryset
            )
        else:
            formset = PropertyOwnerModelFormset(
                request.POST, queryset=property_owner_queryset
            )
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        for form in formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formset):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        category = deal.lead.category
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "category": category,
            "formset": formset,
        }
        return render(self.request, "deals/owner/edit_owner_details.html", ctx)


class EditExecutorDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/owner/edit_executor_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        category = deal_object.lead.category
        if deal_object.lead.user != self.request.user:
            raise Http404
        ctx = {"deal_id": kwargs["deal_id"], "category": category}
        if category == "deceased":
            executor_object = deal_object.lead.property.contact_set.all().filter(
                category="real-estate", sub_category="executor"
            )
            ctx["form_obj"] = RealEstateModelFormset(queryset=executor_object)
        else:
            executor_object = (
                deal_object.lead.property.contact_set.all()
                .filter(category="real-estate", sub_category="agents")
                .first()
            )
            ctx["form"] = RealEstateWithoutMarketForm(instance=executor_object)
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The Executor details have been saved successfully",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:owner_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        category = deal_object.lead.category
        if deal_object.lead.user != self.request.user:
            raise Http404
        property_object = deal_object.lead.property
        if category == "deceased":
            executor_object = property_object.contact_set.all().filter(
                category="real-estate", sub_category="executor"
            )
            form = RealEstateModelFormset(
                request.POST, queryset=executor_object
            )
        else:
            executor_object = (
                property_object.contact_set.all()
                .filter(category="real-estate", sub_category="agents")
                .first()
            )
            form = RealEstateWithoutMarketForm(
                request.POST, instance=executor_object
            )
        if form.is_valid():
            return self.form_valid(form, property_object, category)
        else:
            return self.form_invalid(form, category)

    def form_valid(self, form, property_object, category):
        if category == "deceased":
            for form_instance in form:
                executor_object = form_instance.save(commit=False)
                executor_object._property = property_object
                executor_object.save()
        else:
            executor_object = form.save(commit=False)
            executor_object._property = property_object
            executor_object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, category):
        ctx = {"deal_id": self.kwargs["deal_id"]}
        if category == "deceased":
            ctx["form_obj"] = form
        else:
            ctx["form"] = form
        return render(
            self.request, "deals/owner/edit_executor_details.html", ctx
        )


class EditAgentDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/owner/edit_agent_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        category = deal_object.lead.category
        if deal_object.lead.user != self.request.user:
            raise Http404
        ctx = {"deal_id": kwargs["deal_id"], "category": category}
        executor_object = (
            deal_object.lead.property.contact_set.all()
            .filter(category="real-estate", sub_category="agents")
            .first()
        )
        ctx["form"] = RealEstateWithoutMarketForm(instance=executor_object)
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The Executor details have been saved successfully",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:owner_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        category = deal_object.lead.category
        if deal_object.lead.user != self.request.user:
            raise Http404
        property_object = deal_object.lead.property
        executor_object = (
            property_object.contact_set.all()
            .filter(category="real-estate", sub_category="agents")
            .first()
        )
        form = RealEstateWithoutMarketForm(
            request.POST, instance=executor_object
        )
        if form.is_valid():
            return self.form_valid(form, property_object, category)
        else:
            return self.form_invalid(form, category)

    def form_valid(self, form, property_object, category):
        agent_object = form.save(commit=False)
        agent_object._property = property_object
        agent_object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, category):
        ctx = {"deal_id": self.kwargs["deal_id"], "form": form}
        return render(
            self.request, "deals/owner/edit_executor_details.html", ctx
        )


class EditSolicitorDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/owner/edit_solicitor_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        solicitor_queryset = lead_object.property.contact_set.all().filter(
            category="legal"
        )
        ctx = {
            "deal_id": kwargs["deal_id"],
            "formset": SolicitorModelFormSet(queryset=solicitor_queryset),
            "category": lead_object.category,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The Solicitor details have been saved successfully",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:owner_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__property", "lead__user"
        ).get(pk=kwargs["deal_id"])
        if deal_object.lead.user != self.request.user:
            raise Http404
        property_object = deal_object.lead.property
        solicitor_queryset = property_object.contact_set.all().filter(
            category="legal"
        )
        formset = SolicitorModelFormSet(
            request.POST, queryset=solicitor_queryset
        )
        if formset.is_valid():
            return self.form_valid(formset, property_object)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset, property_object):
        for form_obj in formset:
            solicitor_obj = form_obj.save(commit=False)
            solicitor_obj._property = property_object
            solicitor_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formset):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "formset": formset,
            "category": lead_object.category,
        }
        return render(
            self.request, "deals/owner/edit_solicitor_details.html", ctx
        )


class EditBankDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/owner/edit_bank_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__bank"
        ).get(pk=kwargs["deal_id"])
        if deal_object.lead.user != self.request.user:
            raise Http404
        bank_object = deal_object.lead.property.bank
        ctx = {
            "deal_id": kwargs["deal_id"],
            "form": BankForm(instance=bank_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The Bank details have been saved successfully",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:owner_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__bank"
        ).get(pk=kwargs["deal_id"])
        if deal_object.lead.user != self.request.user:
            raise Http404
        property_object = deal_object.lead.property
        bank_object = property_object.bank
        form = BankForm(request.POST, instance=bank_object)
        if form.is_valid():
            return self.form_valid(form, property_object)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, property_object):
        bank_object = form.save(commit=False)
        bank_object._property = property_object
        bank_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        ctx = {"deal_id": self.kwargs["deal_id"], "form": form}
        return render(self.request, "deals/owner/edit_bank_details.html", ctx)


class InspectionLandDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/inspection/land_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related(
            "lead__user",
            "lead__property__land_details",
            "lead__property__zoning",
            "lead__property__shape",
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        contact_instance = lead_object.property.contact_set.filter(
            sub_category="council"
        ).first()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "land_details_form": LandDetailsForm(
                instance=lead_object.property.land_details,
                prefix="land_details_form",
            ),
            "council_obj": contact_instance,
            "zoning_form": ZoningForm(
                instance=lead_object.property.zoning, prefix="zoning_form"
            ),
            "shape_form": ShapeForm(
                instance=lead_object.property.shape, prefix="shape_form"
            ),
            "property_address_form": PropertyAddressForm(
                instance=lead_object.property, prefix="property_address_form"
            ),
            "council_contact": Contact.objects.filter(
                user=self.request.user, sub_category="council"
            ),
            "contact_id": getattr(contact_instance, "pk", "None"),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        contact_id = request.POST["selected-contact-id"]
        deal = Deal.objects.select_related(
            "lead__user",
            "lead__property__land_details",
            "lead__property__zoning",
            "lead__property__shape",
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        council_contact_obj = Contact.objects.get(pk=contact_id)
        land_details_form = LandDetailsForm(
            request.POST,
            instance=lead_object.property.land_details,
            prefix="land_details_form",
        )
        zoning_form = ZoningForm(
            request.POST,
            instance=lead_object.property.zoning,
            prefix="zoning_form",
        )
        shape_form = ShapeForm(
            request.POST,
            instance=lead_object.property.shape,
            prefix="shape_form",
        )
        property_address_form = PropertyAddressForm(
            request.POST,
            instance=lead_object.property,
            prefix="property_address_form",
        )
        if (
            land_details_form.is_valid()
            and zoning_form.is_valid()
            and shape_form.is_valid()
            and property_address_form.is_valid()
        ):
            return self.form_valid(
                land_details_form,
                council_contact_obj,
                zoning_form,
                shape_form,
                property_address_form,
                lead_object,
            )
        else:
            return self.form_invalid(
                land_details_form,
                council_contact_obj,
                zoning_form,
                shape_form,
                property_address_form,
                contact_id,
            )

    def form_valid(
        self,
        land_details_form,
        council_contact_obj,
        zoning_form,
        shape_form,
        property_address_form,
        lead_object,
    ):
        Contact.objects.filter(
            _property_id=lead_object.property.pk, sub_category="council"
        ).update(_property=None)
        Contact.objects.filter(pk=council_contact_obj.pk).update(
            _property=lead_object.property
        )
        land_details_form.save()
        zoning_form.save()
        shape_form.save()
        property_obj = property_address_form.save(commit=False)
        property_obj.lead = lead_object
        property_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self,
        land_details_form,
        council_contact_obj,
        zoning_form,
        shape_form,
        property_address_form,
        contact_id,
    ):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal.lead
        contact_instance = lead_object.property.contact_set.filter(
            sub_category="council"
        ).first()
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "land_details_form": land_details_form,
            "council_obj": contact_instance,
            "zoning_form": zoning_form,
            "shape_form": shape_form,
            "property_address_form": property_address_form,
            "council_contact": Contact.objects.filter(
                user=self.request.user, sub_category="council"
            ),
            "contact_id": contact_id,
        }
        return render(self.request, "deals/inspection/land_details.html", ctx)


class InspectionLandDetailsSelectedCouncilView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/selected_contact_land_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related(
            "lead__user",
            "lead__property__land_details",
            "lead__property__zoning",
            "lead__property__shape",
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "council_obj": Contact.objects.get(pk=kwargs["contact_id"]),
            "contact_id": kwargs["contact_id"],
        }
        return ctx


class InspectionExternalDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/inspection/external_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related(
            "lead__user",
            "lead__property__street_appeal",
            "lead__property__construction",
            "lead__property__parking",
            "lead__property__features",
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "street_appeal_form": StreetAppealForm(
                instance=lead_object.property.street_appeal,
                prefix="street_appeal_form",
            ),
            "construction_form": ConstructionForm(
                instance=lead_object.property.construction,
                prefix="construction_form",
            ),
            "parking_form": ParkingForm(
                instance=lead_object.property.parking, prefix="parking_form"
            ),
            "features_form": FeaturesForm(
                instance=lead_object.property.features, prefix="features_form"
            ),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_external_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related(
            "lead__user",
            "lead__property__street_appeal",
            "lead__property__construction",
            "lead__property__parking",
            "lead__property__features",
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        street_appeal_form = StreetAppealForm(
            request.POST,
            instance=lead_object.property.street_appeal,
            prefix="street_appeal_form",
        )
        construction_form = ConstructionForm(
            request.POST,
            instance=lead_object.property.construction,
            prefix="construction_form",
        )
        parking_form = ParkingForm(
            request.POST,
            instance=lead_object.property.parking,
            prefix="parking_form",
        )
        features_form = FeaturesForm(
            request.POST,
            instance=lead_object.property.features,
            prefix="features_form",
        )
        if (
            street_appeal_form.is_valid()
            and construction_form.is_valid()
            and parking_form.is_valid()
            and features_form.is_valid()
        ):
            return self.form_valid(
                street_appeal_form,
                construction_form,
                parking_form,
                features_form,
            )
        else:
            return self.form_invalid(
                street_appeal_form,
                construction_form,
                parking_form,
                features_form,
            )

    def form_valid(
        self,
        street_appeal_form,
        construction_form,
        parking_form,
        features_form,
    ):
        street_appeal_form.save()
        construction_form.save()
        parking_form.save()
        features_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self,
        street_appeal_form,
        construction_form,
        parking_form,
        features_form,
    ):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "street_appeal_form": street_appeal_form,
            "construction_form": construction_form,
            "parking_form": parking_form,
            "features_form": features_form,
        }
        return render(
            self.request, "deals/inspection/external_details.html", ctx
        )


class GrannyFlatDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/inspection/granny_flat/granny_flat_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "granny_flat_form": GrannyFlatForm(
                instance=lead_object.property.granny_flat
            ),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        granny_flat_form = GrannyFlatForm(
            request.POST, instance=lead_object.property.granny_flat
        )
        if granny_flat_form.is_valid():
            return self.form_valid(granny_flat_form)
        else:
            return self.form_invalid(granny_flat_form)

    def form_valid(self, granny_flat_form):
        granny_flat_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, granny_flat_form):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "granny_flat_form": granny_flat_form,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/granny_flat_details.html",
            ctx,
        )


class EntryDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The entry has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/entry_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead__property").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        entry_queryset = lead_object.property.entry_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "entry_details_formset": EntryModelFormset(
                queryset=entry_queryset
            ),
            "entry_count": entry_queryset.count(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_entry_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead__property").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        entry_queryset = lead_object.property.entry_set.all()
        entry_details_formset = EntryModelFormset(
            request.POST, queryset=entry_queryset
        )
        if entry_details_formset.is_valid():
            return self.form_valid(entry_details_formset)
        else:
            return self.form_invalid(entry_details_formset)

    def form_valid(self, entry_details_formset):
        for form in entry_details_formset:
            form_obj = form.save(commit=False)
            form_obj.location_name = "Entry"
            form_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, entry_details_formset, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "entry_details_formset": entry_details_formset,
        }
        return render(
            self.request, "deals/inspection/internal/entry_details.html", ctx
        )


class AddEntryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/add/add_entry.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": EntryForm(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_entry_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "lead__property", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        property_object = lead_object.property
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            return self.form_valid(entry_form, property_object, deal_obj)
        else:
            return self.form_invalid(entry_form)

    def form_valid(self, entry_form, property_object, deal_obj):
        entry_object = entry_form.save(commit=False)
        entry_object._property = property_object
        entry_object.location_name = "Entry"
        entry_object.save()
        try:
            Rooms.objects.create(
                renovation=deal_obj.purchase.renovation, entry=entry_object
            )
        except ObjectDoesNotExist:
            Rooms.objects.create(renovation=None, entry=entry_object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, entry_form, *args, **kwargs):
        deal = Deal.objects.select_related("lead").get(pk=kwargs["deal_id"])
        lead_object = deal.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": entry_form,
        }
        return render(
            self.request, "deals/inspection/internal/add/add_entry.html", ctx
        )


class DeleteEntryView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        entry_id = data["entry_id"]
        entry_object = Entry.objects.get(pk=entry_id)
        entry_object.delete()
        response = {"status": 1}
        # Store deletion status in session and check upon redirection. If the message exists, show it to the user that the object has been deleted
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class LoungeDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The lounge has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/lounge_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        lounge_queryset = lead_object.property.lounge_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "lounge_details_formset": LoungeModelFormset(
                queryset=lounge_queryset
            ),
            "lounge_count": lounge_queryset.count(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_lounge_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        lounge_queryset = lead_object.property.lounge_set.all()
        lounge_details_formset = LoungeModelFormset(
            request.POST, queryset=lounge_queryset
        )
        if lounge_details_formset.is_valid():
            return self.form_valid(lounge_details_formset)
        else:
            return self.form_invalid(lounge_details_formset)

    def form_valid(self, lounge_details_formset):
        for form in lounge_details_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, lounge_details_formset):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "lounge_details_formset": lounge_details_formset,
        }
        return render(
            self.request, "deals/inspection/internal/lounge_details.html", ctx
        )


class AddLoungeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/add/add_lounge.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": LoungeForm(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_lounge_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "lead__property", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        property_object = lead_object.property
        lounge_form = LoungeForm(request.POST)
        if lounge_form.is_valid():
            return self.form_valid(lounge_form, property_object, deal_obj)
        else:
            return self.form_invalid(lounge_form)

    def form_valid(self, lounge_form, property_object, deal_obj):
        lounge_object = lounge_form.save(commit=False)
        lounge_object._property = property_object
        lounge_object.location_name = "Lounge"
        lounge_object.save()
        try:
            Rooms.objects.create(
                renovation=deal_obj.purchase.renovation, lounge=lounge_object
            )
        except ObjectDoesNotExist:
            Rooms.objects.create(renovation=None, lounge=lounge_object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, lounge_form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": lounge_form,
        }
        return render(
            self.request, "deals/inspection/internal/add/add_lounge.html", ctx
        )


class DeleteLoungeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        lounge_id = data["lounge_id"]
        lounge_object = Lounge.objects.get(pk=lounge_id)
        lounge_object.delete()
        response = {"status": 1}
        # Store deletion status in session and check upon redirection. If the message exists, show it to the user that the object has been deleted
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class DiningDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The dining has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/dining_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        dining_queryset = lead_object.property.dining_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "dining_details_formset": DiningModelFormset(
                queryset=dining_queryset
            ),
            "dining_count": dining_queryset.count(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_dining_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        dining_queryset = lead_object.property.dining_set.all()
        dining_details_formset = DiningModelFormset(
            request.POST, queryset=dining_queryset
        )
        if dining_details_formset.is_valid():
            return self.form_valid(dining_details_formset)
        else:
            return self.form_invalid(dining_details_formset)

    def form_valid(self, dining_details_formset):
        for form in dining_details_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, dining_details_formset):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "dining_details_formset": dining_details_formset,
        }
        return render(
            self.request, "deals/inspection/internal/dining_details.html", ctx
        )


class AddDiningView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/add/add_dining.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": DiningForm(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_dining_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "lead__property", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        property_object = lead_object.property
        dining_form = DiningForm(request.POST)
        if dining_form.is_valid():
            return self.form_valid(dining_form, property_object, deal_obj)
        else:
            return self.form_invalid(dining_form)

    def form_valid(self, dining_form, property_object, deal_obj):
        dining_object = dining_form.save(commit=False)
        dining_object._property = property_object
        dining_object.location_name = "Dining"
        dining_object.save()
        try:
            Rooms.objects.create(
                renovation=deal_obj.purchase.renovation, dining=dining_object
            )
        except ObjectDoesNotExist:
            Rooms.objects.create(renovation=None, dining=dining_object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, dining_form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": dining_form,
        }
        return render(
            self.request, "deals/inspection/internal/add/add_dining.html", ctx
        )


class DeleteDiningView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        dining_id = data["dining_id"]
        dining_object = Dining.objects.get(pk=dining_id)
        dining_object.delete()
        response = {"status": 1}
        # Store deletion status in session and check upon redirection. If the message exists, show it to the user that the object hsa been deleted
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class KitchenDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/kitchen_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__kitchen"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        kitchen_object = lead_object.property.kitchen
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "kitchen_details_form": KitchenForm(instance=kitchen_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_kitchen_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__kitchen"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        kitchen_object = lead_object.property.kitchen
        kitchen_details_form = KitchenForm(
            request.POST, instance=kitchen_object
        )
        if kitchen_details_form.is_valid():
            return self.form_valid(kitchen_details_form)
        else:
            return self.form_invalid(kitchen_details_form)

    def form_valid(self, kitchen_details_form):
        kitchen_details_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, kitchen_details_form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "kitchen_details_form": kitchen_details_form,
        }
        return render(
            self.request, "deals/inspection/internal/kitchen_details.html", ctx
        )


class LaundryDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/laundry_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        laundry_object = lead_object.property.laundry
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "laundry_details_form": LaundryForm(instance=laundry_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_laundry_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__laundry"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        laundry_object = lead_object.property.laundry
        laundry_details_form = LaundryForm(
            request.POST, instance=laundry_object
        )
        if laundry_details_form.is_valid():
            return self.form_valid(laundry_details_form)
        else:
            return self.form_invalid(laundry_details_form)

    def form_valid(self, laundry_details_form):
        laundry_details_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, laundry_details_form):
        deal_object = Deal.objects.select_related("lead__user").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "laundry_details_form": laundry_details_form,
        }
        return render(
            self.request, "deals/inspection/internal/laundry_details.html", ctx
        )


class BathroomDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The bathroom has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/bathroom_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bathroom_queryset = lead_object.property.bathroom_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bathroom_details_formset": BathroomModelFormset(
                queryset=bathroom_queryset
            ),
            "bathroom_count": bathroom_queryset.count(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_bathroom_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bathroom_queryset = lead_object.property.bathroom_set.all()
        bathroom_details_formset = BathroomModelFormset(
            request.POST, queryset=bathroom_queryset
        )
        if bathroom_details_formset.is_valid():
            return self.form_valid(bathroom_details_formset)
        else:
            return self.form_invalid(bathroom_details_formset)

    def form_valid(self, bathroom_details_formset):
        for form in bathroom_details_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, bathroom_details_formset):
        deal_object = Deal.objects.select_related("lead__user").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bathroom_details_formset": bathroom_details_formset,
        }
        return render(
            self.request,
            "deals/inspection/internal/bathroom_details.html",
            ctx,
        )


class AddBathroomView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/add/add_bathroom.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": BathroomForm(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_bathroom_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        property_object = lead_object.property
        bathroom_form = BathroomForm(request.POST)
        if bathroom_form.is_valid():
            return self.form_valid(bathroom_form, property_object, deal_obj)
        else:
            return self.form_invalid(bathroom_form)

    def form_valid(self, bathroom_form, property_object, deal_obj):
        bathroom_object = bathroom_form.save(commit=False)
        bathroom_object._property = property_object
        bathroom_object.location_name = "Bathroom"
        bathroom_object.save()
        try:
            Rooms.objects.create(
                renovation=deal_obj.purchase.renovation,
                bathroom=bathroom_object,
            )
        except ObjectDoesNotExist:
            Rooms.objects.create(renovation=None, bathroom=bathroom_object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, bathroom_form, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": bathroom_form,
        }
        return render(
            self.request,
            "deals/inspection/internal/add/add_bathroom.html",
            ctx,
        )


class DeleteBathroomView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        bathroom_id = data["bathroom_id"]
        bathroom_object = Bathroom.objects.get(pk=bathroom_id)
        bathroom_object.delete()
        response = {"status": 1}
        # Store deletion status in session and check upon redirection. If the message exists, show it to the user that the object hsa been deleted
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class BedroomDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The bedroom has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/bedroom_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bedroom_queryset = lead_object.property.bedroom_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bedroom_details_formset": BedroomModelFormset(
                queryset=bedroom_queryset
            ),
            "bedroom_count": bedroom_queryset.count(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_bedroom_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bedroom_queryset = lead_object.property.bedroom_set.all()
        bedroom_details_formset = BedroomModelFormset(
            request.POST, queryset=bedroom_queryset
        )
        if bedroom_details_formset.is_valid():
            return self.form_valid(bedroom_details_formset)
        else:
            return self.form_invalid(bedroom_details_formset)

    def form_valid(self, bedroom_details_formset):
        for form in bedroom_details_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, bedroom_details_formset):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bedroom_details_formset": bedroom_details_formset,
        }
        return render(
            self.request, "deals/inspection/internal/bedroom_details.html", ctx
        )


class AddBedroomView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/internal/add/add_bedroom.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": BedroomForm(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_bedroom_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "lead__property", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_obj.lead
        if lead_object.user != self.request.user:
            raise Http404
        property_object = lead_object.property
        bedroom_form = BedroomForm(request.POST)
        if bedroom_form.is_valid():
            return self.form_valid(bedroom_form, property_object, deal_obj)
        else:
            return self.form_invalid(bedroom_form)

    def form_valid(self, bedroom_form, property_object, deal_obj):
        bedroom_object = bedroom_form.save(commit=False)
        bedroom_object._property = property_object
        bedroom_object.location_name = "Bedroom"
        bedroom_object.save()
        try:
            Rooms.objects.create(
                renovation=deal_obj.purchase.renovation, bedroom=bedroom_object
            )
        except ObjectDoesNotExist:
            Rooms.objects.create(renovation=None, bedroom=bedroom_object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, bedroom_form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": bedroom_form,
        }
        return render(
            self.request, "deals/inspection/internal/add/add_bedroom.html", ctx
        )


class DeleteBedroomView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        bedroom_id = data["bedroom_id"]
        bedroom_object = Bedroom.objects.get(pk=bedroom_id)
        bedroom_object.delete()
        response = {"status": 1}
        # Store deletion status in session and check upon redirection. If the message exists, show it to the user that the object hsa been deleted
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class LoanDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/loans/loan_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__bank"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bank_object = lead_object.property.bank
        personal_loan_queryset = lead_object.personalloan_set.all()
        title_queryset = lead_object.title_set.all()
        dealing_queryset = lead_object.dealing_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": BankForm(instance=bank_object),
        }
        if personal_loan_queryset:
            ctx["personal_loan_formset"] = PersonalLoanModelFormset(
                queryset=personal_loan_queryset, prefix="personal_loan_formset"
            )
        else:
            ctx["personal_loan_formset"] = PersonalLoanFormset(
                prefix="personal_loan_formset"
            )
        if title_queryset:
            ctx["title_formset"] = TitleModelFormset(
                queryset=title_queryset, prefix="title_formset"
            )
        else:
            ctx["title_formset"] = TitleFormset(prefix="title_formset")
        if dealing_queryset:
            ctx["dealing_formset"] = DealingModelFormset(
                queryset=dealing_queryset, prefix="dealing_formset"
            )
        else:
            ctx["dealing_formset"] = DealingFormset(prefix="dealing_formset")
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:loan_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__bank"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bank_object = lead_object.property.bank
        personal_loan_queryset = lead_object.personalloan_set.all()
        title_queryset = lead_object.title_set.all()
        dealing_queryset = lead_object.dealing_set.all()
        bank_form = BankForm(request.POST, instance=bank_object)
        personal_loan_formset = PersonalLoanModelFormset(
            request.POST,
            queryset=personal_loan_queryset,
            prefix="personal_loan_formset",
        )
        title_formset = TitleModelFormset(
            request.POST, queryset=title_queryset, prefix="title_formset"
        )
        dealing_formset = DealingModelFormset(
            request.POST, queryset=dealing_queryset, prefix="dealing_formset"
        )
        if (
            bank_form.is_valid()
            and personal_loan_formset.is_valid()
            and title_formset.is_valid()
            and dealing_formset.is_valid()
        ):
            return self.form_valid(
                lead_object,
                bank_form,
                personal_loan_formset,
                title_formset,
                dealing_formset,
            )
        else:
            return self.form_invalid(
                lead_object,
                bank_form,
                personal_loan_formset,
                title_formset,
                dealing_formset,
            )

    def form_valid(
        self,
        lead_object,
        bank_form,
        personal_loan_formset,
        title_formset,
        dealing_formset,
    ):
        if bank_form.has_changed():
            bank_object = bank_form.save()
            bank_object._property = lead_object.property
            bank_object.save()

        # Personal Loan
        personal_loan_list = []
        for loan in lead_object.personalloan_set.all():
            personal_loan_list.append(loan)
        new_personal_loan_list = []
        for formset_form in personal_loan_formset:
            personal_loan_object = formset_form.save(commit=False)
            personal_loan_object.lead = lead_object
            personal_loan_object.save()
            new_personal_loan_list.append(personal_loan_object)
        for loan in personal_loan_list:
            if loan not in new_personal_loan_list:
                loan.delete()
        # Title
        title_list = []
        for title in lead_object.title_set.all():
            title_list.append(title)
        new_title_list = []
        for formset_form in title_formset:
            title_object = formset_form.save(commit=False)
            title_object.lead = lead_object
            title_object.save()
            new_title_list.append(title_object)
        for title in title_list:
            if title not in new_title_list:
                title.delete()
        # Dealing
        dealing_list = []
        for dealing in lead_object.dealing_set.all():
            dealing_list.append(dealing)
        new_dealing_list = []
        for formset_form in dealing_formset:
            dealing_object = formset_form.save(commit=False)
            dealing_object.lead = lead_object
            dealing_object.save()
            new_dealing_list.append(dealing_object)
        for dealing in dealing_list:
            if dealing not in new_dealing_list:
                dealing.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self,
        lead_object,
        bank_form,
        personal_loan_formset,
        title_formset,
        dealing_formset,
    ):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": bank_form,
            "personal_loan_formset": personal_loan_formset,
            "title_formset": title_formset,
            "dealing_formset": dealing_formset,
        }
        return render(self.request, "deals/loans/loan_details.html", ctx)


# Granny Internal Details Views
class GrannyEntryDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/entry_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__entry"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        entry_object = lead_object.property.granny_flat.entry
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": EntryForm(instance=entry_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_entry_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__entry"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        entry_object = lead_object.property.granny_flat.entry
        form = EntryForm(request.POST, instance=entry_object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": form,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/entry_details.html",
            ctx,
        )


class GrannyLoungeDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/lounge_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__lounge"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        lounge_object = lead_object.property.granny_flat.lounge
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": LoungeForm(instance=lounge_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_lounge_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__lounge"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        lounge_object = lead_object.property.granny_flat.lounge
        form = LoungeForm(request.POST, instance=lounge_object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": form,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/lounge_details.html",
            ctx,
        )


class GrannyDiningDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/dining_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__dining"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        dining_object = lead_object.property.granny_flat.dining
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": DiningForm(instance=dining_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_dining_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__dining"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        dining_object = lead_object.property.granny_flat.dining
        form = DiningForm(request.POST, instance=dining_object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": form,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/dining_details.html",
            ctx,
        )


class GrannyKitchenDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/kitchen_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__kitchen"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        kitchen_object = lead_object.property.granny_flat.kitchen
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": KitchenForm(instance=kitchen_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_kitchen_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__kitchen"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        kitchen_object = lead_object.property.granny_flat.kitchen
        form = KitchenForm(request.POST, instance=kitchen_object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": form,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/kitchen_details.html",
            ctx,
        )


class GrannyLaundryDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/laundry_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__laundry"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        laundry_object = lead_object.property.granny_flat.laundry
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": LaundryForm(instance=laundry_object),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_laundry_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat__laundry"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        laundry_object = lead_object.property.granny_flat.laundry
        form = LaundryForm(request.POST, instance=laundry_object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "form": form,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/laundry_details.html",
            ctx,
        )


class GrannyBathroomDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/bathroom_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bathroom_queryset = lead_object.property.granny_flat.bathroom_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bathroom_details_formset": BathroomModelFormset(
                queryset=bathroom_queryset
            ),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_bathroom_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bathroom_queryset = lead_object.property.granny_flat.bathroom_set.all()
        bathroom_details_formset = BathroomModelFormset(
            request.POST, queryset=bathroom_queryset
        )
        if bathroom_details_formset.is_valid():
            return self.form_valid(bathroom_details_formset)
        else:
            return self.form_invalid(bathroom_details_formset)

    def form_valid(self, bathroom_details_formset):
        for form in bathroom_details_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, bathroom_details_formset):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bathroom_details_formset": bathroom_details_formset,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/bathroom_details.html",
            ctx,
        )


class GrannyBedroomDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/inspection/granny_flat/bedroom_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bedroom_queryset = lead_object.property.granny_flat.bedroom_set.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bedroom_details_formset": BedroomModelFormset(
                queryset=bedroom_queryset
            ),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:inspection_granny_flat_bedroom_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_object = Deal.objects.select_related(
            "lead__user", "lead__property__granny_flat"
        ).get(pk=kwargs["deal_id"])
        lead_object = deal_object.lead
        if lead_object.user != self.request.user:
            raise Http404
        bedroom_queryset = lead_object.property.granny_flat.bedroom_set.all()
        bedroom_details_formset = BedroomModelFormset(
            request.POST, queryset=bedroom_queryset
        )
        if bedroom_details_formset.is_valid():
            return self.form_valid(bedroom_details_formset)
        else:
            return self.form_invalid(bedroom_details_formset)

    def form_valid(self, bedroom_details_formset):
        for form in bedroom_details_formset:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, bedroom_details_formset):
        deal_object = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        lead_object = deal_object.lead
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "lead_id": lead_object.id,
            "bedroom_details_formset": bedroom_details_formset,
        }
        return render(
            self.request,
            "deals/inspection/granny_flat/bedroom_details.html",
            ctx,
        )


# Offer Details Views
class PurchaseDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/offer_details/purchase.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        ctx = {
            "form": PurchaseForm(instance=purchase_obj),
            "purchase_costs_formset": PurchaseCostsFormset(
                queryset=purchase_obj.purchasecosts_set.all(),
                prefix="purchase_costs_formset",
            ),
            "holding_costs_formset": HoldingCostsFormset(
                queryset=purchase_obj.holdingcosts_set.all(),
                prefix="holding_costs_formset",
            ),
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:purchase_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user",
            "purchase__renovation",
            "lead__property__parking",
            "lead__property__kitchen",
            "lead__property__laundry",
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        form = PurchaseForm(request.POST, instance=purchase_obj)
        purchase_costs_formset = PurchaseCostsFormset(
            request.POST,
            queryset=purchase_obj.purchasecosts_set.all(),
            prefix="purchase_costs_formset",
        )
        holding_costs_formset = HoldingCostsFormset(
            request.POST,
            queryset=purchase_obj.holdingcosts_set.all(),
            prefix="holding_costs_formset",
        )
        if (
            form.is_valid()
            and purchase_costs_formset.is_valid()
            and holding_costs_formset.is_valid()
        ):
            return self.form_valid(
                request,
                form,
                purchase_costs_formset,
                holding_costs_formset,
                deal_obj,
                purchase_obj,
            )
        else:
            return self.form_invalid(
                form, purchase_costs_formset, holding_costs_formset
            )

    def form_valid(
        self,
        request,
        form,
        purchase_costs_formset,
        holding_costs_formset,
        deal_obj,
        purchase_obj,
    ):
        renovation_required = form.cleaned_data.get(
            "renovation_required", None
        )
        form_obj = form.save()
        form_obj.deal = deal_obj
        form_obj.save()
        # Saving forms of purchase costs formset
        for form in purchase_costs_formset:
            cost_obj = form.save(commit=False)
            cost_obj.purchase = form_obj
            cost_obj.save()
        # Saving forms of holding costs formset
        cost_list = []
        for cost in form_obj.holdingcosts_set.all():
            cost_list.append(cost)
        new_cost_list = []
        for formset_form in holding_costs_formset:
            cost_object = formset_form.save(commit=False)
            cost_object.purchase = form_obj
            cost_object.save()
            new_cost_list.append(cost_object)
        for cost in cost_list:
            if cost not in new_cost_list:
                cost.delete()

        # Update the feasibility report details
        feasibility_report_object = (
            form_obj.feasibilityreport_set.all().first()
        )
        feasibility_report_object.purchase_costs = request.POST.get(
            "purchase_costs_total", 0
        )
        feasibility_report_object.holding_costs = request.POST.get(
            "holding_costs_total", 0
        )
        feasibility_report_object.renovation_costs = (
            form_obj.renovation_allowance
        )
        feasibility_report_object.save()

        # If the Renovated is selected 'Yes' then create a Renovation model object
        if renovation_required == "Yes":
            try:
                if purchase_obj.renovation:
                    pass
            except (AttributeError, Renovation.DoesNotExist):
                Renovation.objects.create(purchase=purchase_obj)
                renovation_obj = purchase_obj.renovation
                Team.objects.create(renovation=renovation_obj)
                # Creating all the Rooms & tasks objects, post Renovation object creation
                property_obj = deal_obj.lead.property
                # Parking
                room_obj = Rooms.objects.create(
                    renovation=renovation_obj, parking=property_obj.parking
                )
                # Entry
                for entry_obj in property_obj.entry_set.all():
                    room_obj = Rooms.objects.create(
                        renovation=renovation_obj, entry=entry_obj
                    )
                # Lounge
                for lounge_obj in property_obj.lounge_set.all():
                    room_obj = Rooms.objects.create(
                        renovation=renovation_obj, lounge=lounge_obj
                    )
                # Dining
                for dining_obj in property_obj.dining_set.all():
                    room_obj = Rooms.objects.create(
                        renovation=renovation_obj, dining=dining_obj
                    )
                # Kitchen
                room_obj = Rooms.objects.create(
                    renovation=renovation_obj, kitchen=property_obj.kitchen
                )
                PrimeCostItems.objects.create(room=room_obj, name="Dishwasher")
                PrimeCostItems.objects.create(room=room_obj, name="Rangehood")
                PrimeCostItems.objects.create(room=room_obj, name="Sink")
                PrimeCostItems.objects.create(room=room_obj, name="Stove")
                PrimeCostItems.objects.create(room=room_obj, name="Tap Ware")
                PrimeCostItems.objects.create(room=room_obj, name="Others")
                # Laundry
                room_obj = Rooms.objects.create(
                    renovation=renovation_obj, laundry=property_obj.laundry
                )
                # Bathroom
                for bathroom_obj in property_obj.bathroom_set.all():
                    room_obj = Rooms.objects.create(
                        renovation=renovation_obj, bathroom=bathroom_obj
                    )
                    PrimeCostItems.objects.create(room=room_obj, name="Basin")
                    PrimeCostItems.objects.create(
                        room=room_obj, name="Bath / Spa"
                    )
                    PrimeCostItems.objects.create(
                        room=room_obj, name="Floor Wastes"
                    )
                    PrimeCostItems.objects.create(
                        room=room_obj, name="Lights / IXL"
                    )
                    PrimeCostItems.objects.create(
                        room=room_obj, name="Mirrors"
                    )
                    PrimeCostItems.objects.create(room=room_obj, name="Shower")
                    PrimeCostItems.objects.create(
                        room=room_obj, name="Tapware & Accessories"
                    )
                    PrimeCostItems.objects.create(
                        room=room_obj, name="Toilets"
                    )
                    PrimeCostItems.objects.create(room=room_obj, name="Vanity")
                    PrimeCostItems.objects.create(room=room_obj, name="Others")
                # Bedroom
                for bedroom_obj in property_obj.bedroom_set.all():
                    room_obj = Rooms.objects.create(
                        renovation=renovation_obj, bedroom=bedroom_obj
                    )

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self, form, purchase_costs_formset, holding_costs_formset
    ):
        deal_obj = Deal.objects.select_related("lead").get(
            lead_id=self.kwargs["deal_id"]
        )
        ctx = {
            "form": form,
            "purchase_costs_formset": purchase_costs_formset,
            "holding_costs_formset": holding_costs_formset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return render(self.request, "deals/offer_details/purchase.html", ctx)


class PurchaseFeasibilityReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/offer_details/purchase_feasibility_report.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        ctx = {
            "form": PurchaseFeasibilityReportForm(
                instance=purchase_obj.feasibilityreport_set.all().first()
            ),
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:purchase_feasibility_report",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        form = PurchaseFeasibilityReportForm(
            request.POST,
            instance=purchase_obj.feasibilityreport_set.all().first(),
        )
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal_obj = Deal.objects.select_related("lead").get(
            lead_id=self.kwargs["deal_id"]
        )
        ctx = {
            "form": form,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return render(
            self.request,
            "deals/offer_details/purchase_feasibility_report.html",
            ctx,
        )


class PurchaseComparableSalesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The Property has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/offer_details/purchase_comparable_sales.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sales_queryset = deal_obj.purchase.comparable_sales.all()
        ctx = {
            "comparable_sales": comparable_sales_queryset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return ctx


class AddPurchaseComparableSaleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/offer_details/add_purchase_comparable_sale.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        ctx = {
            "deal_id": kwargs["deal_id"],
            "form": PurchaseComparableSalesForm,
            "formset": PurchaseComparableSalesImagesFormset,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:purchase_comparable_sales",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        form = PurchaseComparableSalesForm(request.POST)
        formset = PurchaseComparableSalesImagesFormset(
            request.POST, request.FILES
        )
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        deal_obj = Deal.objects.select_related("purchase").get(
            pk=self.kwargs["deal_id"]
        )
        purchase_obj = deal_obj.purchase
        form_obj = form.save(commit=False)
        form_obj.purchase = purchase_obj
        form_obj.save()
        for form in formset:
            if form.cleaned_data.get("image", None):
                image_obj = form.save(commit=False)
                image_obj.comparable_sale = form_obj
                image_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "form": form,
            "formset": formset,
        }
        return render(
            self.request,
            "deals/offer_details/add_purchase_comparable_sale.html",
            ctx,
        )


class PurchaseComparableSaleDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/offer_details/purchase_comparable_sale_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sale_obj = PurchaseComparableSales.objects.get(
            pk=kwargs["comparable_sale_id"]
        )
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "comparable_sale": comparable_sale_obj,
            "images": comparable_sale_obj.images.all(),
        }
        return ctx


class EditPurchaseComparableSaleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/offer_details/edit_purchase_comparable_sale.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sale_obj = PurchaseComparableSales.objects.get(
            pk=kwargs["comparable_sale_id"]
        )
        queryset = comparable_sale_obj.images.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "form": PurchaseComparableSalesForm(instance=comparable_sale_obj),
            "formset": PurchaseComparableSalesImagesModelFormset(
                queryset=queryset if queryset else None
            ),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:purchase_comparable_sales",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sale_obj = PurchaseComparableSales.objects.get(
            pk=kwargs["comparable_sale_id"]
        )
        form = PurchaseComparableSalesForm(
            request.POST, instance=comparable_sale_obj
        )
        formset = PurchaseComparableSalesImagesModelFormset(
            request.POST,
            request.FILES,
            queryset=comparable_sale_obj.images.all(),
        )
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        deal_obj = Deal.objects.select_related("purchase").get(
            pk=self.kwargs["deal_id"]
        )
        purchase_obj = deal_obj.purchase
        form_obj = form.save(commit=False)
        form_obj.purchase = purchase_obj
        form_obj.save()

        image_list = []
        for image in form_obj.images.all():
            image_list.append(image)
        new_image_list = []
        for formset_form in formset:
            if formset_form.cleaned_data.get("image", None):
                image_object = formset_form.save(commit=False)
                image_object.comparable_sale = form_obj
                image_object.save()
                new_image_list.append(image_object)
        for image in image_list:
            if image not in new_image_list:
                image.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "form": form,
            "formset": formset,
        }
        return render(
            self.request,
            "deals/offer_details/edit_purchase_comparable_sale.html",
            ctx,
        )


class DelPurchaseComparableSaleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        comparable_purchase_id = data["comparable_purchase_id"]
        comparable_purchase_obj = PurchaseComparableSales.objects.get(
            pk=comparable_purchase_id
        )
        comparable_purchase_obj.delete()
        response = {"status": True}
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class SaleDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/offer_details/sale.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "sale", "purchase__my_purchase_details"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        my_purchase_details_obj = purchase_obj.my_purchase_details
        sale_obj = deal_obj.sale
        queryset = sale_obj.profitsplit_set.all()
        if queryset:
            formset = ProfitSplitModelFormset(queryset=queryset)
        else:
            formset = ProfitSplitFormset()
        for form in formset:
            form.fields["entity"].queryset = Entity.objects.filter(
                user=self.request.user
            )
        lender_queryset = Contact.objects.filter(
            user=self.request.user, lender=my_purchase_details_obj
        )
        ctx = {
            "form": SaleForm(instance=sale_obj),
            "formset": formset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
            "purchase_price": deal_obj.purchase.maximum_offer,
            "lender_queryset": lender_queryset,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:sale_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "sale").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        sale_obj = deal_obj.sale
        form = SaleForm(request.POST, instance=sale_obj)
        formset = ProfitSplitModelFormset(
            request.POST, queryset=sale_obj.profitsplit_set.all()
        )
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset, deal_obj)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset, deal_obj):
        form_obj = form.save()
        form_obj.deal = deal_obj
        form_obj.save()
        profit_split_list = []
        for entity in form_obj.profitsplit_set.all():
            profit_split_list.append(entity)
        new_profit_split_list = []
        for formset_form in formset:
            if formset_form.cleaned_data.get("entity", None):
                entity_object = formset_form.save(commit=False)
                entity_object.sale = form_obj
                entity_object.save()
                new_profit_split_list.append(entity_object)
        for entity in profit_split_list:
            if entity not in new_profit_split_list:
                entity.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        deal_obj = Deal.objects.select_related(
            "lead", "purchase__my_purchase_details"
        ).get(pk=self.kwargs["deal_id"])
        my_purchase_details_obj = deal_obj.purchase.my_purchase_details
        ctx = {}
        lender_queryset = Contact.objects.filter(
            user=self.request.user, lender=my_purchase_details_obj
        )
        ctx["form"] = form
        ctx["lead_id"] = deal_obj.lead.id
        ctx["deal_id"] = deal_obj.pk
        ctx["formset"] = formset
        ctx["purchase_price"] = deal_obj.purchase.maximum_offer
        ctx["lender_queryset"] = lender_queryset
        return render(self.request, "deals/offer_details/sale.html", ctx)


class SaleComparableSalesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-status", None):
            messages.success(
                self.request,
                "The Property has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-status"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/offer_details/sale_comparable_sales.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "sale").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sales_queryset = deal_obj.sale.comparable_sales.all()
        ctx = {
            "comparable_sales": comparable_sales_queryset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return ctx


class AddSaleComparableSaleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/offer_details/add_sale_comparable_sale.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        ctx = {
            "deal_id": kwargs["deal_id"],
            "form": SaleComparableSalesForm,
            "formset": SaleComparableSalesImagesFormset,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:sale_comparable_sales",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        form = SaleComparableSalesForm(request.POST)
        formset = SaleComparableSalesImagesFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        deal_obj = Deal.objects.select_related("lead__user", "sale").get(
            pk=self.kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        sale_obj = deal_obj.sale
        form_obj = form.save(commit=False)
        form_obj.sale = sale_obj
        form_obj.save()
        for form in formset:
            if form.cleaned_data.get("image", None):
                image_obj = form.save(commit=False)
                image_obj.comparable_sale = form_obj
                image_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "form": form,
            "formset": formset,
        }
        return render(
            self.request,
            "deals/offer_details/add_sale_comparable_sale.html",
            ctx,
        )


class SaleComparableSaleDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/offer_details/sale_comparable_sale_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=self.kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sale_obj = SaleComparableSales.objects.get(
            pk=kwargs["comparable_sale_id"]
        )
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "comparable_sale": comparable_sale_obj,
            "images": comparable_sale_obj.images.all(),
        }
        return ctx


class EditSaleComparableSaleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/offer_details/edit_sale_comparable_sale.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=self.kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sale_obj = SaleComparableSales.objects.get(
            pk=kwargs["comparable_sale_id"]
        )
        queryset = comparable_sale_obj.images.all()
        ctx = {
            "deal_id": kwargs["deal_id"],
            "form": SaleComparableSalesForm(instance=comparable_sale_obj),
            "formset": SaleComparableSalesImagesModelFormset(
                queryset=queryset if queryset else None
            ),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:sale_comparable_sales",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        comparable_sale_obj = SaleComparableSales.objects.get(
            pk=kwargs["comparable_sale_id"]
        )
        form = SaleComparableSalesForm(
            request.POST, instance=comparable_sale_obj
        )
        formset = SaleComparableSalesImagesModelFormset(
            request.POST,
            request.FILES,
            queryset=comparable_sale_obj.images.all(),
        )
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        deal_obj = Deal.objects.select_related("sale").get(
            pk=self.kwargs["deal_id"]
        )
        sale_obj = deal_obj.sale
        form_obj = form.save(commit=False)
        form_obj.sale = sale_obj
        form_obj.save()

        image_list = []
        for image in form_obj.images.all():
            image_list.append(image)
        new_image_list = []
        for formset_form in formset:
            if formset_form.cleaned_data.get("image", None):
                image_object = formset_form.save(commit=False)
                image_object.comparable_sale = form_obj
                image_object.save()
                new_image_list.append(image_object)
        for image in image_list:
            if image not in new_image_list:
                image.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        ctx = {
            "deal_id": self.kwargs["deal_id"],
            "form": form,
            "formset": formset,
        }
        return render(
            self.request,
            "deals/offer_details/edit_sale_comparable_sale.html",
            ctx,
        )


class DelSaleComparableSaleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        comparable_sale_id = data["comparable_sale_id"]
        comparable_sale_obj = SaleComparableSales.objects.get(
            pk=comparable_sale_id
        )
        comparable_sale_obj.delete()
        response = {"status": True}
        request.session["deletion-status"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


# For showing renovation details as the user clicks on Renovation in deals_navbar
class RenovationDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/renovation_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "renovation_obj": Renovation.objects.select_related("purchase")
            .filter(purchase=deal_obj.purchase)
            .first(),
            "form": RenovationForm(instance=deal_obj.purchase.renovation),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        form = RenovationForm(
            request.POST, instance=deal_obj.purchase.renovation
        )
        if form.is_valid():
            return self.form_valid(form, deal_obj)
        else:
            return self.form_invalid(form, deal_obj)

    def form_valid(self, form, deal_obj):
        form_obj = form.save()
        form_obj.purchase = deal_obj.purchase
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, deal_obj):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "form": form,
            "renovation_obj": Renovation.objects.filter(
                purchase=deal_obj.purchase
            ).first(),
        }
        return render(
            self.request, "deals/renovation/renovation_details.html", ctx
        )


class RenovationTeamView(LoginRequiredMixin, View):
    """
    View for showing all the available contacts in a team of renovation
    """

    def get(self, request, *args, **kwargs):
        if request.session.get("member-deletion-success", None):
            messages.success(
                self.request,
                "The member has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["member-deletion-success"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/renovation_team.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation__team"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        team_obj = deal_obj.purchase.renovation.team
        team_contacts = team_obj.contact.all()
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "contacts": team_contacts,
        }
        return ctx


class AddRenovationTeamView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/add_renovation_team.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "form": SearchContactForm(),
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The member has been added successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_team",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        form = SearchContactForm(request.POST)
        if form.is_valid():
            return self.form_valid(form, deal_obj)
        else:
            return self.form_invalid(form, deal_obj)

    def form_valid(self, form, deal_obj):
        query_id = form.cleaned_data["search_contact_id"]
        team_obj, created = Team.objects.get_or_create(
            renovation=deal_obj.purchase.renovation
        )
        if not team_obj.contact.filter(id=query_id).exists():
            team_obj.contact.add(Contact.objects.get(pk=query_id))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, deal_obj):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "form": form,
        }
        return render(
            self.request, "deals/renovation/add_renovation_team.html", ctx
        )


class FetchRenovationTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        content = request.body
        data = json.loads(content.decode("utf-8"))
        search_query = data["search_query"]
        contacts = Contact.objects.filter(
            sub_category__icontains=search_query, user=self.request.user
        )
        filtered_contacts = contacts.exclude(
            id__in=Team.objects.filter(
                renovation=deal_obj.purchase.renovation
            )[0].contact.all()
        )
        response_list = []
        for contact in filtered_contacts[0:10]:
            response_list.append(
                {
                    "id": contact.pk,
                    "details": str(contact.contact_name)
                    + " - "
                    + str(contact.sub_category),
                }
            )
        return HttpResponse(
            json.dumps(response_list), content_type="application/json"
        )


class DeleteRenovationTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        member_id = data["member_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation__team"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        team_obj = deal_obj.purchase.renovation.team
        member_obj = Contact.objects.get(pk=member_id)
        team_obj.contact.remove(member_obj)
        response = {"status": True}
        request.session["member-deletion-success"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class ConfirmRenovationTeamView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        deal_id = kwargs["deal_id"]
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=deal_id
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        if Renovation.objects.filter(purchase=deal_obj.purchase).exists():
            response = {"status": "redirect"}
        else:
            response = {"status": "alert"}
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class RenovationRoomsView(LoginRequiredMixin, View):
    """
    View for showing all available rooms as soon as the user clicks on Rooms tab in Renovation
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/renovation_rooms.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "rooms": Rooms.objects.filter(
                renovation=deal_obj.purchase.renovation, parking=None
            ),
        }
        return ctx


class RenovationRoomsDetailsView(LoginRequiredMixin, View):
    """
    When user clicks on a particular table row in rooms table then he gets redirected to rooms details page.
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/renovation_rooms_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        room_id = kwargs["room_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_obj = renovation_obj.rooms
        rooms_form = RoomsDetailsForm(instance=rooms_obj.get(pk=room_id))
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_obj.all(),
            "selected_room_form": rooms_form,
        }
        return ctx

    def get_success_url(self, room_id):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_rooms_details",
            kwargs={"deal_id": self.kwargs["deal_id"], "room_id": room_id},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        room_id = request.POST["selected-room-id"]
        renovation_obj = deal_obj.purchase.renovation
        rooms_obj = renovation_obj.rooms
        rooms_form = RoomsDetailsForm(
            request.POST, instance=rooms_obj.get(pk=room_id)
        )
        if rooms_form.is_valid():
            return self.form_valid(rooms_form, room_id)
        else:
            return self.form_invalid(rooms_form, deal_obj, room_id, rooms_obj)

    def form_valid(self, rooms_form, room_id):
        rooms_form.save()
        return HttpResponseRedirect(self.get_success_url(room_id))

    def form_invalid(self, rooms_form, deal_obj, room_id, rooms_obj):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_obj.all(),
            "selected_room_form": rooms_form,
        }
        return render(
            self.request, "deals/renovation/renovation_rooms_details.html", ctx
        )


class RenovationImagesView(LoginRequiredMixin, View):
    """
    View for showing all available rooms as soon as the user clicks on Rooms tab in Renovation
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/renovation_images.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "before_renovation_images": Images.objects.filter(
                renovation=deal_obj.purchase.renovation
            ).filter(category="Before-Renovation"),
            "after_renovation_images": Images.objects.filter(
                renovation=deal_obj.purchase.renovation
            ).filter(category="After-Renovation"),
        }
        return ctx


class AddOrEditRenovationImagesView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            "deals/renovation/add_or_edit_renovation_images.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        ctx = {"lead_id": deal_obj.lead.pk, "deal_id": deal_obj.pk}
        renovation_category = kwargs["category"]
        if renovation_category == "before-renovation":
            before_renovation_images = Images.objects.filter(
                renovation=renovation_obj
            ).filter(category="Before-Renovation")
            if not before_renovation_images:
                ctx["formset"] = ImagesFormset()
            else:
                ctx["formset"] = ImagesModelFormset(
                    queryset=before_renovation_images
                )
        elif renovation_category == "after-renovation":
            after_renovation_images = Images.objects.filter(
                renovation=renovation_obj
            ).filter(category="After-Renovation")
            if not after_renovation_images:
                ctx["formset"] = ImagesFormset()
            else:
                ctx["formset"] = ImagesModelFormset(
                    queryset=after_renovation_images
                )
        else:
            raise Http404
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_images",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        if kwargs["category"] == "before-renovation":
            renovation_category = "Before-Renovation"
            renovation_images_queryset = Images.objects.filter(
                renovation=renovation_obj
            ).filter(category=renovation_category)
        else:
            renovation_category = "After-Renovation"
            renovation_images_queryset = Images.objects.filter(
                renovation=renovation_obj
            ).filter(category=renovation_category)
        formset = ImagesModelFormset(
            request.POST, request.FILES, queryset=renovation_images_queryset
        )
        if formset.is_valid():
            return self.form_valid(
                formset, renovation_obj, renovation_category
            )
        else:
            return self.form_invalid(formset, deal_obj)

    def form_valid(self, formset, renovation_obj, renovation_category):
        image_list = []
        for image in renovation_obj.images.all().filter(
            category=renovation_category
        ):
            image_list.append(image)
        new_image_list = []
        for formset_form in formset:
            if formset_form.cleaned_data.get("image", None):
                image_object = formset_form.save(commit=False)
                image_object.renovation = renovation_obj
                image_object.category = renovation_category
                image_object.save()
                new_image_list.append(image_object)
        for image in image_list:
            if image not in new_image_list:
                image.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formset, deal_obj):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "formset": formset,
        }
        return render(
            self.request,
            "deals/renovation/add_or_edit_renovation_images.html",
            ctx,
        )


class RenderRenovationImageFormView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "deals/renovation/renovation_images_form.html",
            {"form": ImagesForm(prefix="form-" + str(kwargs["form_id"]))},
        )


class RenovationRoomsTasksView(LoginRequiredMixin, View):
    """
    When user clicks on tasks tab in a particular room then all tasks related to that room will be shown
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            "deals/renovation/renovation_rooms_tasks_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        room_id = kwargs["room_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_obj = renovation_obj.rooms
        rooms_form = RoomsForm(instance=rooms_obj.get(pk=room_id))
        # tasks_form = TasksForm(instance=rooms_obj.get(pk=room_id).tasks.all().first())
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        ctx = {
            "tasks_formset": {},
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_obj.all(),
            "selected_room_form": rooms_form,
        }  # For initaiting second level dict
        for member in team_members:
            tasks_query_set = Tasks.objects.filter(
                room=Rooms.objects.get(pk=room_id)
            ).filter(service_man=member)
            if tasks_query_set:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    TasksModelFormset(
                        prefix="tasks_" + str(member.pk),
                        queryset=tasks_query_set,
                    ),
                )
            else:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    TasksFormset(prefix="tasks_" + str(member.pk)),
                )
        internal_tasks_for_myself = rooms_obj.get(
            pk=room_id
        ).tasks_for_myself.all()
        if internal_tasks_for_myself:
            ctx[
                "internal_tasks_for_myself_formset"
            ] = InternalTasksForMyselfModelFormset(
                queryset=internal_tasks_for_myself,
                prefix="internal_tasks_for_myself",
            )
        else:
            ctx[
                "internal_tasks_for_myself_formset"
            ] = InternalTasksForMyselfFormset(
                prefix="internal_tasks_for_myself"
            )
        return ctx

    def get_success_url(self, room_id):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_rooms_tasks_details",
            kwargs={"deal_id": self.kwargs["deal_id"], "room_id": room_id},
        )

    def post(self, request, *args, **kwargs):
        room_id = request.POST["selected-room-id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_obj = renovation_obj.rooms
        rooms_form = RoomsForm(
            request.POST, instance=rooms_obj.get(pk=room_id)
        )
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        tasks_forms = {}
        for member in team_members:
            tasks_query_set = Tasks.objects.filter(
                room=Rooms.objects.get(pk=room_id)
            ).filter(service_man=member)
            tasks_forms["form-" + str(member.pk)] = TasksModelFormset(
                request.POST,
                prefix="tasks_" + str(member.pk),
                queryset=tasks_query_set,
            )
        for form_name, formset in tasks_forms.items():
            if formset.is_valid():
                result = True
                continue
            else:
                result = False
                break
        internal_tasks_for_myself = rooms_obj.get(
            pk=room_id
        ).tasks_for_myself.all()
        internal_tasks_for_myself_formset = InternalTasksForMyselfModelFormset(
            request.POST,
            queryset=internal_tasks_for_myself,
            prefix="internal_tasks_for_myself",
        )
        if (
            result
            and rooms_form.is_valid()
            and internal_tasks_for_myself_formset.is_valid()
        ):
            return self.form_valid(
                rooms_form,
                tasks_forms,
                room_id,
                internal_tasks_for_myself_formset,
                renovation_obj,
            )
        return self.form_invalid(
            rooms_form,
            tasks_forms,
            deal_obj,
            room_id,
            rooms_obj,
            team_members,
            internal_tasks_for_myself_formset,
        )

    def form_valid(  # NOQA: C901
        self,
        rooms_form,
        tasks_forms_dict,
        room_id,
        internal_tasks_for_myself_formset,
        renovation_obj,
    ):
        rooms_form_obj = rooms_form.save()
        for form_name, tasks_formset in tasks_forms_dict.items():
            contact_id = form_name.split("-")[-1]
            tasks_query_set = Tasks.objects.filter(
                room=room_id, service_man=contact_id
            )
            tasks_list = []
            for tasks in tasks_query_set:
                tasks_list.append(tasks)
            new_tasks_list = []
            for form in tasks_formset:
                task_form_obj = form.save(commit=False)
                task_form_obj.room = rooms_form_obj
                task_form_obj.service_man = Contact.objects.get(
                    pk=int(contact_id)
                )
                task_form_obj.save()
                new_tasks_list.append(task_form_obj)
            for task in tasks_list:
                if task not in new_tasks_list:
                    task.delete()

        tasks_query_set = rooms_form_obj.tasks_for_myself.all()
        tasks_list = []
        for tasks in tasks_query_set:
            tasks_list.append(tasks)
        new_tasks_list = []
        for form in internal_tasks_for_myself_formset:
            task_form_obj = form.save(commit=False)
            task_form_obj.room = rooms_form_obj
            task_form_obj.save()
            new_tasks_list.append(task_form_obj)
        for task in tasks_list:
            if task not in new_tasks_list:
                task.delete()

        # Calculate the total amount for all the tasks for this external location
        current_expenses = 0
        for t in rooms_form_obj.tasks.all():
            string = ""
            if t.total:
                for i in t.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for m in rooms_form_obj.materials.all():
            string = ""
            if m.total:
                for i in m.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        rooms_form_obj.room_total_cost = current_expenses
        budget = rooms_form_obj.room_budget
        string = ""
        if budget:
            for i in budget:
                if i.isdigit() or i == ".":
                    string += i
            budget = float(string)
            rooms_form_obj.room_difference = (
                budget - rooms_form_obj.room_total_cost
            )
            rooms_form_obj.save()

        renovation_obj.current_expenses = method_for_calculating_current_expenses(
            self.kwargs["deal_id"]
        )
        renovation_obj.save()

        return HttpResponseRedirect(self.get_success_url(room_id))

    def form_invalid(
        self,
        rooms_form,
        tasks_forms,
        deal_obj,
        room_id,
        rooms_obj,
        team_members,
        internal_tasks_for_myself_formset,
    ):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_obj.all(),
            "selected_room_form": rooms_form,
            "tasks_formset": {},
            "internal_tasks_for_myself_formset": internal_tasks_for_myself_formset,
        }
        for form_name, formset in tasks_forms.items():
            ctx["tasks_formset"][
                "tasks_formset_" + str(form_name.split("-")[-1])
            ] = [Contact.objects.get(pk=form_name.split("-")[-1]), formset]
        return render(
            self.request,
            "deals/renovation/renovation_rooms_tasks_details.html",
            ctx,
        )


class RenovationRoomsSelectDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        room_id = kwargs["room_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_obj = renovation_obj.rooms
        rooms_form = RoomsDetailsForm(instance=rooms_obj.get(pk=room_id))
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        ctx = {
            "tasks_formset": {},
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_obj.all(),
            "selected_room_form": rooms_form,
        }
        for member in team_members:
            tasks_query_set = Tasks.objects.filter(
                room=Rooms.objects.get(pk=room_id)
            ).filter(service_man=member)
            if tasks_query_set:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    TasksModelFormset(
                        prefix="tasks_" + str(member.pk),
                        queryset=tasks_query_set,
                    ),
                )
            else:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    TasksFormset(prefix="tasks_" + str(member.pk)),
                )
        return render(
            request, "deals/renovation/renovation_select_details.html", ctx
        )


class RenovationRoomsTasksSelectDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        room_id = kwargs["room_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_obj = renovation_obj.rooms
        rooms_form = RoomsForm(instance=rooms_obj.get(pk=room_id))
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        ctx = {
            "tasks_formset": {},
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_obj.all(),
            "selected_room_form": rooms_form,
        }
        for member in team_members:
            tasks_query_set = Tasks.objects.filter(
                room=Rooms.objects.get(pk=room_id)
            ).filter(service_man=member)
            if tasks_query_set:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    TasksModelFormset(
                        prefix="tasks_" + str(member.pk),
                        queryset=tasks_query_set,
                    ),
                )
            else:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    TasksFormset(prefix="tasks_" + str(member.pk)),
                )
        internal_tasks_for_myself = rooms_obj.get(
            pk=room_id
        ).tasks_for_myself.all()
        if internal_tasks_for_myself:
            ctx[
                "internal_tasks_for_myself_formset"
            ] = InternalTasksForMyselfModelFormset(
                queryset=internal_tasks_for_myself,
                prefix="internal_tasks_for_myself",
            )
        else:
            ctx[
                "internal_tasks_for_myself_formset"
            ] = InternalTasksForMyselfFormset(
                prefix="internal_tasks_for_myself"
            )
        return render(
            request,
            "deals/renovation/renovation_tasks_select_details.html",
            ctx,
        )


class MyPurchaseDetailsView(LoginRequiredMixin, View):
    """
    This view will be used to add and edit my details for the purchase of a property
    """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(self, *args, **kwargs)
        return render(request, "deals/my_purchase_details.html", context)

    def get_context_data(self, *args, **kwargs):
        context = {}
        deal_obj = Deal.objects.select_related(
            "lead__user",
            "purchase__my_purchase_details__entity",
            "purchase__my_purchase_details__accountant",
            "purchase__my_purchase_details__agent",
            "purchase__my_purchase_details__conveyancer",
            "purchase__my_purchase_details__bank",
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        my_purchase_details_obj = purchase_obj.my_purchase_details
        entity_obj = my_purchase_details_obj.entity
        property_private_lenders = my_purchase_details_obj.my_lender_details.order_by(
            "pk"
        )
        all_private_lenders = Contact.objects.filter(
            user=self.request.user, sub_category="money-backers"
        )
        contacts_queryset = Contact.objects.filter(user=self.request.user)
        form = MyPurchaseDetailsForm(instance=my_purchase_details_obj)
        form.fields["entity"].queryset = Entity.objects.filter(
            user=self.request.user
        )
        form.fields["accountant"].queryset = contacts_queryset.filter(
            sub_category="accountants"
        )
        form.fields["agent"].queryset = Agent.objects.filter(
            created_by=self.request.user
        )
        form.fields["conveyancer"].queryset = contacts_queryset.filter(
            sub_category="conveyancers"
        )
        context["form"] = form
        context["deal_id"] = deal_obj.id
        context["lead_id"] = deal_obj.lead.id
        context["accountant"] = my_purchase_details_obj.accountant
        context["agent"] = my_purchase_details_obj.agent
        context["conveyancer"] = my_purchase_details_obj.conveyancer
        context["entity"] = entity_obj
        context["bank_obj"] = my_purchase_details_obj.bank
        context["all_private_lenders"] = all_private_lenders
        context["private_lender_queryset"] = property_private_lenders
        return context

    def get_success_url(self):
        if self.request.POST.get("bank_status", None) == "bank":
            return reverse_lazy(
                "dashboard:deals:add_or_edit_bank_details",
                kwargs={"deal_id": self.kwargs["deal_id"]},
            )
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:my_purchase_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        selected_lender_id = request.POST.getlist("selected-lender-id")
        unique_selected_lender_id = set(selected_lender_id)
        deal_obj = Deal.objects.select_related(
            "lead__user",
            "purchase__my_purchase_details__bank",
            "purchase__my_purchase_details__conveyancer",
            "purchase__my_purchase_details__entity",
            "purchase__my_purchase_details__accountant",
            "purchase__my_purchase_details__agent",
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        my_purchase_details_obj = purchase_obj.my_purchase_details
        all_private_lenders = Contact.objects.filter(
            user=self.request.user, sub_category="money-backers"
        )
        pre_selected_private_lenders = my_purchase_details_obj.my_lender_details.order_by(
            "pk"
        )
        form = MyPurchaseDetailsForm(
            request.POST, instance=my_purchase_details_obj
        )
        feasibility_report_object = (
            purchase_obj.feasibilityreport_set.all().first()
        )
        if form.is_valid():
            return self.form_valid(
                form,
                my_purchase_details_obj,
                all_private_lenders,
                pre_selected_private_lenders,
                unique_selected_lender_id,
                feasibility_report_object,
            )
        else:
            return self.form_invalid(form, my_purchase_details_obj)

    def form_valid(
        self,
        form,
        my_purchase_details_obj,
        all_private_lenders,
        pre_selected_private_lenders,
        unique_selected_lender_id,
        feasibility_report_object,
    ):
        new_my_details_obj = form.save(commit=False)
        new_my_details_obj.bank = my_purchase_details_obj.bank
        new_my_details_obj.save()
        for lender_obj in pre_selected_private_lenders:
            Contact.objects.filter(pk=lender_obj.pk).update(lender=None)
        for lender_id in unique_selected_lender_id:
            Contact.objects.filter(pk=lender_id).update(
                lender=new_my_details_obj
            )
        lender_queryset = Contact.objects.filter(
            user=self.request.user, lender=my_purchase_details_obj.id
        )
        total_amount = 0
        for lender_obj in lender_queryset:
            total_amount += self.calc_value(lender_obj.total_approx)
        count = 1
        new_total_amount = ""
        for digit in str(total_amount)[::-1]:
            new_total_amount += str(digit)
            if count % 3 == 0:
                new_total_amount += ","
            count += 1
        # feasibility_report_object.money_partner = new_total_amount[::-1]
        # feasibility_report_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def calc_value(self, value):
        if value:
            value = int("".join(value.split(",")))
        else:
            value = 0
        return value

    def form_invalid(self, form, my_purchase_details_obj):
        context = {}
        deal_obj = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        entity_obj = my_purchase_details_obj.entity
        property_private_lenders = my_purchase_details_obj.my_lender_details.order_by(
            "pk"
        )
        all_private_lenders = Contact.objects.filter(
            user=self.request.user, sub_category="money-backers"
        )
        context["form"] = form
        context["deal_id"] = deal_obj.id
        context["lead_id"] = deal_obj.lead.id
        context["accountant"] = my_purchase_details_obj.accountant
        context["agent"] = my_purchase_details_obj.agent
        context["conveyancer"] = my_purchase_details_obj.conveyancer
        context["entity"] = entity_obj
        context["bank_obj"] = my_purchase_details_obj.bank
        context["all_private_lenders"] = all_private_lenders
        context["private_lender_queryset"] = property_private_lenders
        return render(self.request, "deals/my_purchase_details.html", context)


class EditLenderDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "deals/render-my-details/edit_lender_details.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        ctx = {}
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        contact_object = Contact.objects.get(pk=kwargs["lender_id"])
        ctx["deal_id"] = deal_obj.id
        ctx["lead_id"] = deal_obj.lead.id
        ctx["form"] = PrivateLenderForm(instance=contact_object)
        ctx["lender_obj"] = contact_object
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "Payment Details updated successfully",
            extra_tags="lender_edited",
        )
        return reverse_lazy(
            "dashboard:deals:my_purchase_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        lender_object = Contact.objects.get(pk=kwargs["lender_id"])
        purchase_obj = deal_obj.purchase
        my_purchase_details_obj = purchase_obj.my_purchase_details
        feasibility_report_object = (
            purchase_obj.feasibilityreport_set.all().first()
        )
        form = PrivateLenderForm(request.POST, instance=lender_object)
        if form.is_valid():
            return self.form_valid(
                form,
                deal_obj,
                feasibility_report_object,
                my_purchase_details_obj,
            )
        else:
            return self.form_invalid(form, deal_obj, lender_object)

    def form_valid(
        self,
        form,
        deal_obj,
        feasibility_report_object,
        my_purchase_details_obj,
    ):
        form_object = form.save(commit=False)
        if form_object.payment_type == "Interest ROI":
            form_object.profit_split = None
        else:
            form_object.investment_amount = None
            form_object.agreed_interest_rate_per_annum = None
            form_object.duration_in_months = None
            form_object.roi_approx = None
            form_object.total_approx = None
        form_object.user = self.request.user
        form_object.lender = my_purchase_details_obj
        form_object.save()
        my_purchase_details_obj.money_lender = "Private Lender"
        my_purchase_details_obj.save()
        lender_queryset = Contact.objects.filter(
            user=self.request.user, lender=my_purchase_details_obj.id
        )
        total_amount = 0
        for lender_obj in lender_queryset:
            total_amount += self.calc_value(lender_obj.total_approx)
        count = 1
        new_total_amount = ""
        for digit in str(total_amount)[::-1]:
            new_total_amount += str(digit)
            if count % 3 == 0:
                new_total_amount += ","
            count += 1
        # feasibility_report_object.money_partner = new_total_amount[::-1]
        # feasibility_report_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def calc_value(self, value):
        if value:
            value = int("".join(value.split(",")))
        else:
            value = 0
        return value

    def form_invalid(self, form, deal_obj, lender_object):
        ctx = {
            "form": form,
            "lender_obj": lender_object,
            "deal_id": deal_obj.id,
            "lead_id": deal_obj.lead.id,
        }
        return render(
            self.request,
            "deals/render-my-details/edit_lender_details.html",
            ctx,
        )


class RemoveLenderDetailsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        contact_id = data["lender_id"]
        Contact.objects.filter(pk=contact_id).update(lender=None)
        response = {"status": True}
        request.session["deletion-success"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class RenderLenderDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        deal_obj = Deal.objects.select_related(
            "lead__user",
            "purchase__my_purchase_details__entity",
            "purchase__my_purchase_details__accountant",
            "purchase__my_purchase_details__agent",
            "purchase__my_purchase_details__conveyancer",
            "purchase__my_purchase_details__bank",
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        context["private_lender"] = Contact.objects.get(pk=kwargs["lender_id"])
        return render(
            request, "deals/render-my-details/lender-details.html", context
        )


class RenderEntityDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "deals/render-my-details/entity-details.html",
            {"entity": Entity.objects.get(pk=kwargs["entity_id"])},
        )


class RenderContactDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "deals/render-my-details/contact-details.html",
            {"contact": Contact.objects.get(pk=kwargs["contact_id"])},
        )


class AddOrEditBankView(LoginRequiredMixin, View):
    """
    When user clicks on add or edit bank details button, this view is called
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(self.request, "deals/add_or_edit_bank_details.html", ctx)

    def get_context_data(self, *args, **kwargs):
        ctx = {}
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__my_purchase_details__bank"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        my_purchase_details_obj = purchase_obj.my_purchase_details
        bank_obj = my_purchase_details_obj.bank
        if bank_obj:
            ctx["form"] = MyBankDetailsForm(instance=bank_obj)
        else:
            ctx["form"] = MyBankDetailsForm()
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:my_purchase_details",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__my_purchase_details__bank"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        my_purchase_details_obj = purchase_obj.my_purchase_details
        bank_obj = my_purchase_details_obj.bank
        if bank_obj:
            form = MyBankDetailsForm(request.POST, instance=bank_obj)
        else:
            form = MyBankDetailsForm(request.POST)
        if form.is_valid():
            return self.form_valid(form, my_purchase_details_obj)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, my_purchase_details_obj):
        bank_obj = form.save()
        my_purchase_details_obj.bank = bank_obj
        my_purchase_details_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        ctx = {"form": form}
        return render(self.request, "deals/add_or_edit_bank_details.html", ctx)


class RenovationRoomsMaterialsView(LoginRequiredMixin, View):
    """
    When user clicks on Material tab in a particular room then all Materials related to that room will be shown
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            "deals/renovation/renovation_rooms_materials_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        room_id = kwargs["room_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_queryset = renovation_obj.rooms
        rooms_obj = rooms_queryset.get(pk=room_id)
        rooms_form = RoomsForm(instance=rooms_obj)
        materials_queryset = rooms_obj.materials.all()
        prime_cost_items_queryset = ""
        if rooms_obj.kitchen or rooms_obj.bathroom:
            prime_cost_items_queryset = rooms_obj.prime_cost_items.all()
        ctx = dict()
        if materials_queryset:
            ctx["materials_formset"] = MaterialsModelFormset(
                queryset=materials_queryset, prefix="materials_formset"
            )
        else:
            ctx["materials_formset"] = MaterialsFormset(
                prefix="materials_formset"
            )
        ctx["lead_id"] = deal_obj.lead.pk
        ctx["deal_id"] = deal_obj.pk
        ctx["room_id"] = room_id
        ctx["all_rooms"] = rooms_queryset.all()
        ctx["selected_room_form"] = rooms_form
        if prime_cost_items_queryset:
            ctx["prime_cost_items_formset"] = PrimeCostItemsFormset(
                queryset=prime_cost_items_queryset,
                prefix="prime_cost_items_formset",
            )
        return ctx

    def get_success_url(self, room_id):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_rooms_materials_details",
            kwargs={"deal_id": self.kwargs["deal_id"], "room_id": room_id},
        )

    def post(self, request, *args, **kwargs):
        room_id = request.POST["selected-room-id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_queryset = renovation_obj.rooms
        rooms_obj = rooms_queryset.get(pk=room_id)
        rooms_form = RoomsForm(request.POST, instance=rooms_obj)
        materials_queryset = rooms_obj.materials.all()
        materials_formset = MaterialsModelFormset(
            request.POST,
            queryset=materials_queryset,
            prefix="materials_formset",
        )
        prime_cost_items_formset = None
        validate = True
        if rooms_obj.kitchen or rooms_obj.bathroom:
            prime_cost_items_queryset = rooms_obj.prime_cost_items.all()
            prime_cost_items_formset = PrimeCostItemsFormset(
                request.POST,
                queryset=prime_cost_items_queryset,
                prefix="prime_cost_items_formset",
            )
            if not prime_cost_items_formset.is_valid():
                validate = False

        if rooms_form.is_valid() and materials_formset.is_valid() and validate:
            prime_cost_items_formset = (
                prime_cost_items_formset if validate else False
            )
            return self.form_valid(
                rooms_form,
                materials_formset,
                room_id,
                validate,
                prime_cost_items_formset,
                renovation_obj,
            )
        return self.form_invalid(
            rooms_form,
            materials_formset,
            room_id,
            deal_obj,
            rooms_queryset,
            validate,
            prime_cost_items_formset,
        )

    def form_valid(  # NOQA: C901
        self,
        rooms_form,
        materials_formset,
        room_id,
        validate,
        prime_cost_items_formset,
        renovation_obj,
    ):
        rooms_form_obj = rooms_form.save()
        materials_queryset = Materials.objects.filter(room=room_id)
        materials_list = []
        for material in materials_queryset:
            materials_list.append(material)
        new_materials_list = []
        for form in materials_formset:
            material_form_obj = form.save(commit=False)
            material_form_obj.room = rooms_form_obj
            material_form_obj.save()
            new_materials_list.append(material_form_obj)
        for material in materials_list:
            if material not in new_materials_list:
                material.delete()
        if validate:
            for form in prime_cost_items_formset:
                prime_cost_items_form_obj = form.save(commit=False)
                prime_cost_items_form_obj.room = rooms_form_obj
                prime_cost_items_form_obj.save()

        # Calculate the total amount for all the tasks for this external location
        current_expenses = 0
        for t in rooms_form_obj.tasks.all():
            string = ""
            if t.total:
                for i in t.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for m in rooms_form_obj.materials.all():
            string = ""
            if m.total:
                for i in m.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for p in rooms_form_obj.prime_cost_items.all():
            string = ""
            if p.total:
                for i in p.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        rooms_form_obj.room_total_cost = current_expenses
        budget = rooms_form_obj.room_budget
        string = ""
        if budget:
            for i in budget:
                if i.isdigit() or i == ".":
                    string += i
            budget = float(string)
            rooms_form_obj.room_difference = (
                budget - rooms_form_obj.room_total_cost
            )
            rooms_form_obj.save()

        renovation_obj.current_expenses = method_for_calculating_current_expenses(
            self.kwargs["deal_id"]
        )
        renovation_obj.save()

        return HttpResponseRedirect(self.get_success_url(room_id))

    def form_invalid(
        self,
        rooms_form,
        materials_formset,
        room_id,
        deal_obj,
        rooms_queryset,
        validate,
        prime_cost_items_formset,
    ):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "room_id": room_id,
            "all_rooms": rooms_queryset.all(),
            "selected_room_form": rooms_form,
            "materials_formset": materials_formset,
        }
        if prime_cost_items_formset is not None:
            ctx["prime_cost_items_formset"] = prime_cost_items_formset
        return render(
            self.request,
            "deals/renovation/renovation_rooms_materials_details.html",
            ctx,
        )


class RenovationRoomsMaterialsSelectDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        room_id = kwargs["room_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        rooms_queryset = renovation_obj.rooms
        room_obj = rooms_queryset.get(pk=room_id)
        rooms_form = RoomsForm(instance=room_obj)
        materials_queryset = room_obj.materials.all()
        prime_cost_items_queryset = ""
        if room_obj.kitchen or room_obj.bathroom:
            prime_cost_items_queryset = room_obj.prime_cost_items.all()
        ctx = dict()
        ctx["lead_id"] = deal_obj.lead.pk
        ctx["deal_id"] = deal_obj.pk
        ctx["room_id"] = room_id
        ctx["all_rooms"] = rooms_queryset.all()
        ctx["selected_room_form"] = rooms_form
        if materials_queryset:
            ctx["materials_formset"] = MaterialsModelFormset(
                queryset=materials_queryset, prefix="materials_formset"
            )
        else:
            ctx["materials_formset"] = MaterialsFormset(
                prefix="materials_formset"
            )
        if prime_cost_items_queryset:
            ctx["prime_cost_items_formset"] = PrimeCostItemsFormset(
                queryset=prime_cost_items_queryset,
                prefix="prime_cost_items_formset",
            )
        return render(
            request,
            "deals/renovation/renovation_material_select_details.html",
            ctx,
        )


class PurchaseCorrespondanceDocumentsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/correspondance/purchase_correspondance_documents.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        correspondance_documents_queryset = (
            purchase_obj.purchase_correspondance_documents.all()
        )
        ctx = {
            "correspondance_documents_queryset": correspondance_documents_queryset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return ctx


class AddOrEditPurchaseCorrespondanceDocumentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/correspondance/add_or_edit_purchase_correspondance_documents.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        correspondance_documents_queryset = (
            purchase_obj.purchase_correspondance_documents.all()
        )
        ctx = {}
        if correspondance_documents_queryset:
            ctx[
                "correspondance_documents_formset"
            ] = PurchaseCorrespondanceDocumentsModelFormset(
                queryset=correspondance_documents_queryset,
                prefix="purchase_documents_formset",
            )
        else:
            ctx[
                "correspondance_documents_formset"
            ] = PurchaseCorrespondanceDocumentsFormset(
                prefix="purchase_documents_formset"
            )
        ctx["lead_id"] = deal_obj.lead.id
        ctx["deal_id"] = deal_obj.pk
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:purchase_correspondance_documents",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user", "purchase").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        correspondance_documents_queryset = (
            purchase_obj.purchase_correspondance_documents.all()
        )
        formset = PurchaseCorrespondanceDocumentsModelFormset(
            request.POST,
            request.FILES,
            queryset=correspondance_documents_queryset,
            prefix="purchase_documents_formset",
        )
        if formset.is_valid():
            return self.form_valid(
                request,
                formset,
                correspondance_documents_queryset,
                purchase_obj,
            )
        else:
            return self.form_invalid(formset)

    def form_valid(
        self, request, formset, correspondance_documents_queryset, purchase_obj
    ):
        documents_list = []
        for document in correspondance_documents_queryset:
            documents_list.append(document)
        new_documents_list = []
        for form in formset:
            document_form_obj = form.save(commit=False)
            document_form_obj.purchase = purchase_obj
            document_form_obj.save()
            new_documents_list.append(document_form_obj)
        for document in documents_list:
            if document not in new_documents_list:
                document.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formset):
        deal_obj = Deal.objects.select_related("lead").get(
            lead_id=self.kwargs["deal_id"]
        )
        ctx = {
            "correspondance_documents_formset": formset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return render(
            self.request,
            "deals/correspondance/add_or_edit_purchase_correspondance_documents.html",
            ctx,
        )


class RenderPurchaseDocumentFormView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "deals/correspondance/purchase_document_form.html",
            {
                "form": PurchaseCorrespondanceDocumentsForm(
                    prefix="purchase_documents_formset-"
                    + str(kwargs["form_id"])
                )
            },
        )


class DownloadPurchaseCorrespondanceDocument(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        document_id = kwargs["document_id"]
        document_obj = PurchaseCorrespondanceDocuments.objects.get(
            pk=document_id
        )
        document = document_obj.document
        extension = document_obj.document.name.split(".")[
            -1
        ]  # To get the extension of the file uploaded by the user
        if extension in ["jpg", "jpeg", "png"]:
            response = HttpResponse(
                content=document, content_type="image/" + extension
            )
        elif extension == "pdf":
            response = HttpResponse(
                content=document, content_type="application/pdf"
            )
        elif extension in ["txt", "text"]:
            response = HttpResponse(
                content=document, content_type="text/plain"
            )
        elif extension in ["doc", "docx", "dot", "dotx"]:
            response = HttpResponse(
                content=document, content_type="application/msword"
            )
        else:
            response = HttpResponse(content=document)
        response["Content-Disposition"] = "attachment; filename={}".format(
            document.name
        )
        return response


class RenovationExternalView(LoginRequiredMixin, View):
    """
    View for showing all available locations as soon as the user clicks on External tab in Renovation
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request, "deals/renovation/renovation_external.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal_obj.lead.user != self.request.user:
            raise Http404
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "external_locations": External.objects.filter(
                renovation=deal_obj.purchase.renovation
            ),
        }
        return ctx


class AddOrEditExternalLocationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request,
            "deals/renovation/add_or_edit_external_locations.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        purchase_obj = deal_obj.purchase
        external_locations_queryset = purchase_obj.renovation.external.all()
        ctx = {}
        if external_locations_queryset:
            ctx["external_locations_formset"] = ExternalLocationModelFormset(
                queryset=external_locations_queryset,
                prefix="external_locations_formset",
            )
        else:
            ctx["external_locations_formset"] = ExternalLocationFormset(
                prefix="external_locations_formset"
            )
        ctx["lead_id"] = deal_obj.lead.id
        ctx["deal_id"] = deal_obj.pk
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_external",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        external_locations_queryset = renovation_obj.external.all()
        formset = ExternalLocationModelFormset(
            request.POST,
            queryset=external_locations_queryset,
            prefix="external_locations_formset",
        )
        if formset.is_valid():
            return self.form_valid(
                request, formset, external_locations_queryset, renovation_obj
            )
        else:
            return self.form_invalid(formset)

    def form_valid(
        self, request, formset, external_locations_queryset, renovation_obj
    ):
        locations_list = []
        for location in external_locations_queryset:
            locations_list.append(location)
        new_locations_list = []
        for form in formset:
            location_form_obj = form.save(commit=False)
            location_form_obj.renovation = renovation_obj
            location_form_obj.save()
            new_locations_list.append(location_form_obj)
        for location in locations_list:
            if location not in new_locations_list:
                location.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formset):
        deal_obj = Deal.objects.select_related("lead").get(
            lead_id=self.kwargs["deal_id"]
        )
        ctx = {
            "external_locations_formset": formset,
            "lead_id": deal_obj.lead.id,
            "deal_id": deal_obj.pk,
        }
        return render(
            self.request,
            "deals/renovation/add_or_edit_external_locations.html",
            ctx,
        )


class RenovationExternalLocationDetailsView(LoginRequiredMixin, View):
    """
    When user clicks on a particular table row in locations table then he gets redirected to location details page.
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            "deals/renovation/renovation_location_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        location_id = kwargs["location_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_form = ExternalDetailsForm(
            instance=locations_queryset.get(pk=location_id)
        )
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
        }
        return ctx

    def get_success_url(self, location_id):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_external_location_details",
            kwargs={
                "deal_id": self.kwargs["deal_id"],
                "location_id": location_id,
            },
        )

    def post(self, request, *args, **kwargs):
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        location_id = request.POST["selected-location-id"]
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_form = ExternalDetailsForm(
            request.POST, instance=locations_queryset.get(pk=location_id)
        )
        if locations_form.is_valid():
            return self.form_valid(locations_form, location_id)
        else:
            return self.form_invalid(
                locations_form, deal_obj, location_id, locations_queryset
            )

    def form_valid(self, locations_form, location_id):
        locations_form.save()
        return HttpResponseRedirect(self.get_success_url(location_id))

    def form_invalid(
        self, locations_form, deal_obj, location_id, locations_queryset
    ):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
        }
        return render(
            self.request,
            "deals/renovation/renovation_location_details.html",
            ctx,
        )


class RenovationExternalLocationSelectDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        location_id = kwargs["location_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_form = ExternalDetailsForm(
            instance=locations_queryset.get(pk=location_id)
        )
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
        }
        return render(
            request,
            "deals/renovation/renovation_external_location_select_details.html",
            ctx,
        )


class RenovationExternalLocationTasksView(LoginRequiredMixin, View):
    """
    When user clicks on tasks tab in a particular location then all tasks related to that location will be shown
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            "deals/renovation/renovation_external_locations_tasks_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        location_id = kwargs["location_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_form = ExternalForm(
            instance=locations_queryset.get(pk=location_id)
        )
        # tasks_form = ExternalTasksForm(instance=locations_queryset.get(pk=location_id).tasks.all().first())
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        ctx = {
            "tasks_formset": {"k1": ["tasks_formset", "member"]},
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
        }
        for member in team_members:
            tasks_query_set = ExternalTasks.objects.filter(
                location=External.objects.get(pk=location_id)
            ).filter(service_man=member)
            if tasks_query_set:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    ExternalTasksModelFormset(
                        prefix="tasks_" + str(member.pk),
                        queryset=tasks_query_set,
                    ),
                )
            else:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    ExternalTasksFormset(prefix="tasks_" + str(member.pk)),
                )
        external_tasks_for_myself = locations_queryset.get(
            pk=location_id
        ).external_tasks_for_myself.all()
        if external_tasks_for_myself:
            ctx[
                "external_tasks_for_myself_formset"
            ] = ExternalTasksForMyselfModelFormset(
                queryset=external_tasks_for_myself,
                prefix="external_tasks_for_myself",
            )
        else:
            ctx[
                "external_tasks_for_myself_formset"
            ] = ExternalTasksForMyselfFormset(
                prefix="external_tasks_for_myself"
            )
        return ctx

    def get_success_url(self, location_id):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_external_location_tasks_details",
            kwargs={
                "deal_id": self.kwargs["deal_id"],
                "location_id": location_id,
            },
        )

    def post(self, request, *args, **kwargs):
        location_id = request.POST["selected-location-id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_form = ExternalForm(
            request.POST, instance=locations_queryset.get(pk=location_id)
        )
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        tasks_forms = {}
        for member in team_members:
            tasks_query_set = ExternalTasks.objects.filter(
                location=External.objects.get(pk=location_id)
            ).filter(service_man=member)
            tasks_forms["form-" + str(member.pk)] = ExternalTasksModelFormset(
                request.POST,
                prefix="tasks_" + str(member.pk),
                queryset=tasks_query_set,
            )
        for form_name, formset in tasks_forms.items():
            if formset.is_valid():
                result = True
                continue
            else:
                result = False
                break
        external_tasks_for_myself = locations_queryset.get(
            pk=location_id
        ).external_tasks_for_myself.all()
        external_tasks_for_myself_formset = ExternalTasksForMyselfModelFormset(
            request.POST,
            queryset=external_tasks_for_myself,
            prefix="external_tasks_for_myself",
        )
        if (
            result
            and locations_form.is_valid()
            and external_tasks_for_myself_formset.is_valid()
        ):
            return self.form_valid(
                locations_form,
                tasks_forms,
                location_id,
                external_tasks_for_myself_formset,
                renovation_obj,
            )
        return self.form_invalid(
            locations_form,
            tasks_forms,
            deal_obj,
            location_id,
            locations_queryset,
            team_members,
            external_tasks_for_myself_formset,
        )

    def form_valid(  # NOQA: C901
        self,
        locations_form,
        tasks_forms_dict,
        location_id,
        external_tasks_for_myself_formset,
        renovation_obj,
    ):
        locations_form_obj = locations_form.save()
        for form_name, tasks_formset in tasks_forms_dict.items():
            contact_id = form_name.split("-")[-1]
            tasks_query_set = ExternalTasks.objects.filter(
                location=location_id, service_man=contact_id
            )
            tasks_list = []
            for tasks in tasks_query_set:
                tasks_list.append(tasks)
            new_tasks_list = []
            for form in tasks_formset:
                task_form_obj = form.save(commit=False)
                task_form_obj.location = locations_form_obj
                task_form_obj.service_man = Contact.objects.get(
                    pk=int(contact_id)
                )
                task_form_obj.save()
                new_tasks_list.append(task_form_obj)
            for task in tasks_list:
                if task not in new_tasks_list:
                    task.delete()

        tasks_query_set = locations_form_obj.external_tasks_for_myself.all()
        tasks_list = []
        for tasks in tasks_query_set:
            tasks_list.append(tasks)
        new_tasks_list = []
        for form in external_tasks_for_myself_formset:
            task_form_obj = form.save(commit=False)
            task_form_obj.location = locations_form_obj
            task_form_obj.save()
            new_tasks_list.append(task_form_obj)
        for task in tasks_list:
            if task not in new_tasks_list:
                task.delete()

        # Calculate the total amount for all the tasks for this external location
        current_expenses = 0
        for t in locations_form_obj.external_tasks.all():
            string = ""
            if t.total:
                for i in t.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for m in locations_form_obj.external_materials.all():
            string = ""
            if m.total:
                for i in m.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        locations_form_obj.total_cost = current_expenses
        budget = locations_form_obj.budget
        string = ""
        if budget:
            for i in budget:
                if i.isdigit() or i == ".":
                    string += i
            budget = float(string)
            locations_form_obj.difference = (
                budget - locations_form_obj.total_cost
            )
            locations_form_obj.save()

        renovation_obj.current_expenses = method_for_calculating_current_expenses(
            self.kwargs["deal_id"]
        )
        renovation_obj.save()
        return HttpResponseRedirect(self.get_success_url(location_id))

    def form_invalid(
        self,
        locations_form,
        tasks_forms,
        deal_obj,
        location_id,
        locations_queryset,
        team_members,
        external_tasks_for_myself_formset,
    ):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
            "tasks_formset": {},
            "external_tasks_for_myself_formset": external_tasks_for_myself_formset,
        }
        for form_name, formset in tasks_forms.items():
            ctx["tasks_formset"][
                "tasks_formset_" + str(form_name.split("-")[-1])
            ] = [Contact.objects.get(pk=form_name.split("-")[-1]), formset]

        return render(
            self.request,
            "deals/renovation/renovation_external_locations_tasks_details.html",
            ctx,
        )


class RenovationExternalLocationTasksSelectDetailsView(
    LoginRequiredMixin, View
):
    def get(self, request, *args, **kwargs):
        location_id = kwargs["location_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_form = ExternalForm(
            instance=locations_queryset.get(pk=location_id)
        )
        team_members = Team.objects.filter(renovation=renovation_obj)[
            0
        ].contact.all()
        ctx = {
            "tasks_formset": {},
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
        }
        for member in team_members:
            tasks_query_set = ExternalTasks.objects.filter(
                location=External.objects.get(pk=location_id)
            ).filter(service_man=member)
            if tasks_query_set:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    ExternalTasksModelFormset(
                        prefix="tasks_" + str(member.pk),
                        queryset=tasks_query_set,
                    ),
                )
            else:
                ctx["tasks_formset"]["tasks_formset_" + str(member.pk)] = (
                    member,
                    ExternalTasksFormset(prefix="tasks_" + str(member.pk)),
                )
        external_tasks_for_myself = locations_queryset.get(
            pk=location_id
        ).external_tasks_for_myself.all()
        if external_tasks_for_myself:
            ctx[
                "external_tasks_for_myself_formset"
            ] = ExternalTasksForMyselfModelFormset(
                queryset=external_tasks_for_myself,
                prefix="external_tasks_for_myself",
            )
        else:
            ctx[
                "external_tasks_for_myself_formset"
            ] = ExternalTasksForMyselfFormset(
                prefix="external_tasks_for_myself"
            )
        return render(
            request,
            "deals/renovation/renovation_external_location_tasks_select_details.html",
            ctx,
        )


class RenovationExternalLocationMaterialsView(LoginRequiredMixin, View):
    """
    When user clicks on Material tab in a particular location then all Materials related to that location will be shown
    """

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            self.request,
            "deals/renovation/renovation_external_location_materials_details.html",
            ctx,
        )

    def get_context_data(self, *args, **kwargs):
        location_id = kwargs["location_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_obj = locations_queryset.get(pk=location_id)
        locations_form = ExternalForm(instance=locations_obj)
        materials_queryset = locations_obj.external_materials.all()
        ctx = dict()
        if materials_queryset:
            ctx["materials_formset"] = ExternalMaterialsModelFormset(
                queryset=materials_queryset, prefix="materials_formset"
            )
        else:
            ctx["materials_formset"] = ExternalMaterialsFormset(
                prefix="materials_formset"
            )
        ctx["lead_id"] = deal_obj.lead.pk
        ctx["deal_id"] = deal_obj.pk
        ctx["location_id"] = location_id
        ctx["all_locations"] = locations_queryset.all()
        ctx["selected_location_form"] = locations_form
        return ctx

    def get_success_url(self, location_id):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:renovation_external_location_materials_details",
            kwargs={
                "deal_id": self.kwargs["deal_id"],
                "location_id": location_id,
            },
        )

    def post(self, request, *args, **kwargs):
        location_id = request.POST["selected-location-id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        locations_obj = locations_queryset.get(pk=location_id)
        locations_form = ExternalForm(request.POST, instance=locations_obj)
        materials_queryset = locations_obj.external_materials.all()
        materials_formset = ExternalMaterialsModelFormset(
            request.POST,
            queryset=materials_queryset,
            prefix="materials_formset",
        )
        if locations_form.is_valid() and materials_formset.is_valid():
            return self.form_valid(
                locations_form, materials_formset, location_id, renovation_obj
            )
        else:
            return self.form_invalid(
                locations_form,
                materials_formset,
                location_id,
                deal_obj,
                locations_queryset,
            )

    def form_valid(
        self, locations_form, materials_formset, location_id, renovation_obj
    ):
        locations_form_obj = locations_form.save()
        materials_queryset = ExternalMaterials.objects.filter(
            location=location_id
        )
        materials_list = []
        for material in materials_queryset:
            materials_list.append(material)
        new_materials_list = []
        for form in materials_formset:
            material_form_obj = form.save(commit=False)
            material_form_obj.location = locations_form_obj
            material_form_obj.save()
            new_materials_list.append(material_form_obj)
        for material in materials_list:
            if material not in new_materials_list:
                material.delete()

        current_expenses = 0
        for t in locations_form_obj.external_tasks.all():
            string = ""
            if t.total:
                for i in t.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for m in locations_form_obj.external_materials.all():
            string = ""
            if m.total:
                for i in m.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        locations_form_obj.total_cost = current_expenses
        budget = locations_form_obj.budget
        string = ""
        if budget:
            for i in budget:
                if i.isdigit() or i == ".":
                    string += i
            budget = float(string)
            locations_form_obj.difference = (
                budget - locations_form_obj.total_cost
            )
            locations_form_obj.save()

        renovation_obj.current_expenses = method_for_calculating_current_expenses(
            self.kwargs["deal_id"]
        )
        renovation_obj.save()

        return HttpResponseRedirect(self.get_success_url(location_id))

    def form_invalid(
        self,
        locations_form,
        materials_formset,
        location_id,
        deal_obj,
        locations_queryset,
    ):
        ctx = {
            "lead_id": deal_obj.lead.pk,
            "deal_id": deal_obj.pk,
            "location_id": location_id,
            "all_locations": locations_queryset.all(),
            "selected_location_form": locations_form,
            "materials_formset": materials_formset,
        }
        return render(
            self.request,
            "deals/renovation/renovation_external_location_materials_details.html",
            ctx,
        )


class RenovationExternalLocationMaterialsSelectDetailsView(
    LoginRequiredMixin, View
):
    def get(self, request, *args, **kwargs):
        location_id = kwargs["location_id"]
        deal_obj = Deal.objects.select_related(
            "lead__user", "purchase__renovation"
        ).get(pk=kwargs["deal_id"])
        if deal_obj.lead.user != self.request.user:
            raise Http404
        renovation_obj = deal_obj.purchase.renovation
        locations_queryset = renovation_obj.external
        location_obj = locations_queryset.get(pk=location_id)
        locations_form = ExternalForm(instance=location_obj)
        materials_queryset = location_obj.external_materials.all()
        ctx = dict()
        ctx["lead_id"] = deal_obj.lead.pk
        ctx["deal_id"] = deal_obj.pk
        ctx["location_id"] = location_id
        ctx["all_locations"] = locations_queryset.all()
        ctx["selected_location_form"] = locations_form
        if materials_queryset:
            ctx["materials_formset"] = ExternalMaterialsModelFormset(
                queryset=materials_queryset, prefix="materials_formset"
            )
        else:
            ctx["materials_formset"] = ExternalMaterialsFormset(
                prefix="materials_formset"
            )
        return render(
            request,
            "deals/renovation/renovation_external_location_material_select_details.html",
            ctx,
        )


class RemindersListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.session.get("deletion-success", None):
            messages.success(
                self.request,
                "The Reminder has been deleted successfully!",
                extra_tags="deleted",
            )
            del request.session["deletion-success"]
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/reminders/reminders_list.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        reminders = Reminders.objects.filter(deal=deal)
        ctx = {
            "reminders": reminders,
            "lead_id": deal.lead.pk,
            "deal_id": deal.pk,
        }
        return ctx


class AddReminderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/reminders/add_reminder.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        ctx = {
            "form": ReminderForm(),
            "lead_id": deal.lead.pk,
            "deal_id": deal.pk,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:reminders_list",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        form = ReminderForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        deal = Deal.objects.select_related("lead__user").get(
            pk=self.kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        reminder_obj = form.save(commit=False)
        reminder_obj.deal = deal
        reminder_obj.user = self.request.user
        reminder_obj.datetime = datetime.combine(
            form.cleaned_data["date"], form.cleaned_data["time"]
        )
        reminder_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        ctx = {"form": form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
        return render(self.request, "deals/reminders/add_reminder.html", ctx)


class EditReminderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/reminders/edit_reminder.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        reminder = Reminders.objects.get(pk=kwargs["reminder_id"])
        ctx = {}
        form = ReminderForm(
            {
                "date": reminder.datetime.date,
                "time": reminder.datetime.time,
                "notes": reminder.notes,
            },
            instance=reminder,
        )
        ctx["form"] = form
        ctx["lead_id"] = deal.lead.pk
        ctx["deal_id"] = deal.pk
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:reminders_list",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        reminder = Reminders.objects.get(pk=kwargs["reminder_id"])
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        deal = Deal.objects.select_related("lead__user").get(
            pk=self.kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        reminder_obj = form.save(commit=False)
        reminder_obj.deal = deal
        reminder_obj.user = self.request.user
        reminder_obj.datetime = datetime.combine(
            form.cleaned_data["date"], form.cleaned_data["time"]
        )
        reminder_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        ctx = {"form": form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
        return render(self.request, "deals/reminders/edit_reminder.html", ctx)


class DeleteReminderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.body
        data = json.loads(content.decode("utf-8"))
        reminder_id = data["reminder_id"]
        reminder_obj = Reminders.objects.get(pk=reminder_id)
        reminder_obj.delete()
        response = {"status": True}
        request.session["deletion-success"] = True
        return HttpResponse(
            json.dumps(response), content_type="application/json"
        )


class AFCAComplaintLodgedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/loans/afca_complaint_lodged.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user", "lead").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        afca_complaint_lodged = AFCAComplaintLodged.objects.filter(deal=deal)
        if afca_complaint_lodged:
            afca_complaint_lodged_form = AFCAComplaintLodgedForm(
                instance=afca_complaint_lodged.first()
            )
        else:
            afca_complaint_lodged_form = AFCAComplaintLodgedForm()
        ctx = {
            "form": afca_complaint_lodged_form,
            "lead_id": deal.lead.pk,
            "deal_id": deal.pk,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:afca_complaint_lodged",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        afca_complaint_lodged = AFCAComplaintLodged.objects.filter(deal=deal)
        if afca_complaint_lodged:
            afca_complaint_lodged_form = AFCAComplaintLodgedForm(
                request.POST, instance=afca_complaint_lodged.first()
            )
        else:
            afca_complaint_lodged_form = AFCAComplaintLodgedForm(request.POST)
        if afca_complaint_lodged_form.is_valid():
            return self.form_valid(afca_complaint_lodged_form)
        else:
            return self.form_invalid(afca_complaint_lodged_form)

    def form_valid(self, form):
        deal = Deal.objects.get(pk=self.kwargs["deal_id"])
        afca_obj = form.save(commit=False)
        afca_obj.deal = deal
        afca_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        ctx = {"form": form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
        return render(
            self.request, "deals/loans/afca_complaint_lodged.html", ctx
        )


class ListForSaleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/list_for_sale.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        list_for_sale = ListForSale.objects.filter(deal=deal)
        if list_for_sale:
            list_for_sale_form = ListForSaleForm(
                instance=list_for_sale.first()
            )
        else:
            list_for_sale_form = ListForSaleForm()
        list_for_sale_form.fields[
            "agent"
        ].queryset = Agent.objects.filter(
            created_by=self.request.user
        )
        ctx = {
            "form": list_for_sale_form,
            "lead_id": deal.lead.pk,
            "deal_id": deal.pk,
        }
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:list_for_sale",
            kwargs={"deal_id": self.kwargs["deal_id"]},
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        list_for_sale = ListForSale.objects.filter(deal=deal)
        if list_for_sale:
            list_for_sale_form = ListForSaleForm(
                request.POST, instance=list_for_sale.first()
            )
        else:
            list_for_sale_form = ListForSaleForm(request.POST)
        if list_for_sale_form.is_valid():
            return self.form_valid(list_for_sale_form)
        else:
            return self.form_invalid(list_for_sale_form)

    def form_valid(self, form):
        deal = Deal.objects.get(pk=self.kwargs["deal_id"])
        list_for_sale_obj = form.save(commit=False)
        list_for_sale_obj.deal = deal
        list_for_sale_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        deal = Deal.objects.select_related("lead").get(
            pk=self.kwargs["deal_id"]
        )
        ctx = {"form": form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
        return render(self.request, "deals/list_for_sale.html", ctx)


class SoldView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "deals/sold.html", ctx)

    def get_context_data(self, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        sold = Sold.objects.filter(deal=deal)
        if sold:
            sold_form = SoldForm(instance=sold.first())
        else:
            sold_form = SoldForm()
        ctx = {"form": sold_form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully!",
            extra_tags="submitted",
        )
        return reverse_lazy(
            "dashboard:deals:sold", kwargs={"deal_id": self.kwargs["deal_id"]}
        )

    def post(self, request, *args, **kwargs):
        deal = Deal.objects.select_related("lead__user").get(
            pk=kwargs["deal_id"]
        )
        if deal.lead.user != self.request.user:
            raise Http404
        sold = Sold.objects.filter(deal=deal)
        if sold:
            sold_form = SoldForm(request.POST, instance=sold.first())
        else:
            sold_form = SoldForm(request.POST)
        if sold_form.is_valid():
            return self.form_valid(sold_form)
        else:
            return self.form_invalid(deal, sold_form)

    def form_valid(self, form):
        deal = Deal.objects.get(pk=self.kwargs["deal_id"])
        list_for_sale_obj = form.save(commit=False)
        list_for_sale_obj.deal = deal
        list_for_sale_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, deal, form):
        ctx = {"form": form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
        return render(self.request, "deals/sold.html", ctx)


def method_for_calculating_current_expenses(deal_id):  # NOQA: C901
    """
    This method is used to calculate the total current expenses for the given deal_id
    """
    deal_obj = Deal.objects.select_related("purchase__renovation").get(
        pk=deal_id
    )
    renovation_obj = deal_obj.purchase.renovation
    rooms = renovation_obj.rooms.all()
    external = renovation_obj.external.all()
    current_expenses = 0
    for r in rooms:
        for t in r.tasks.all():
            string = ""
            if t.total:
                for i in t.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for m in r.materials.all():
            string = ""
            if m.total:
                for i in m.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for p in r.prime_cost_items.all():
            string = ""
            if p.total:
                for i in p.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

    for e in external:
        for t in e.external_tasks.all():
            string = ""
            if t.total:
                for i in t.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

        for m in e.external_materials.all():
            string = ""
            if m.total:
                for i in m.total:
                    if i.isdigit() or i == ".":
                        string += i
                current_expenses += float(string)

    return current_expenses

from .models import Solicitor,Agent,BankNew,Executor,Family,Liquidator,Family,Other
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
#Solicitor 
class SolicitorListView(ListView):
    model=Solicitor
    fields = '__all__'

        
class SolicitorCreateView(CreateView):
    model=Solicitor
    fields = '__all__'
   

class SolicitorUpdateView(UpdateView):
    model=Solicitor
    fields = '__all__'
    template_name = "deals/solicitor_form_edit.html"

class SolicitorDeleteView(DeleteView):
    model=Solicitor
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:solicitorlist')
    
#Agent   
class AgentListView(ListView):
    model=Agent
    fields = '__all__'
        
class AgentCreateView(CreateView):
    model=Agent
    fields = '__all__'
   

class AgentUpdateView(UpdateView):
    model=Agent
    fields = '__all__'
    template_name = "deals/agent_form_edit.html"
    
        
class AgentDeleteView(DeleteView):
    model=Agent
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:agentlist')    


#Bank
class BankListView(ListView):
    model=BankNew
    fields = '__all__'
        
class BankCreateView(CreateView):
    model=BankNew
    fields = '__all__'
   

class BankUpdateView(UpdateView):
    model=BankNew
    fields = '__all__'
    template_name = "deals/bank_form_edit.html"
    
        
class BankDeleteView(DeleteView):
    model=BankNew
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:banklist')    
    
#Executor
class ExecutorListView(ListView):
    model=Executor
    fields = '__all__'
        
class ExecutorCreateView(CreateView):
    model=Executor
    fields = '__all__'
   

class ExecutorUpdateView(UpdateView):
    model=Executor
    fields = '__all__'
    template_name = "deals/executor_form_edit.html"
    
        
class ExecutorDeleteView(DeleteView):
    model=Executor
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:executorlist') 
    
#Family

class FamilyListView(ListView):
    model=Family
    fields = '__all__'
        
class FamilyCreateView(CreateView):
    model=Family
    fields = '__all__'
   

class FamilyUpdateView(UpdateView):
    model=Family
    fields = '__all__'
    template_name = "deals/family_form_edit.html"
    
        
class FamilyDeleteView(DeleteView):
    model=Family
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:familylist') 
    
#Liquidator

class LiquidatorListView(ListView):
    model=Liquidator
    fields = '__all__'
        
class LiquidatorCreateView(CreateView):
    model=Liquidator
    fields = '__all__'
   

class LiquidatorUpdateView(UpdateView):
    model=Liquidator
    fields = '__all__'
    template_name = "deals/liquidator_form_edit.html"
    
        
class LiquidatorDeleteView(DeleteView):
    model=Liquidator
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:liquidatorlist') 
    
#Other
class OtherListView(ListView):
    model=Other
    fields = '__all__'
    template_name='deals/other/other_list.html'
        
class OtherCreateView(CreateView):
    model=Other
    fields = '__all__'
    template_name='deals/other/other_form.html'
   

class OtherUpdateView(UpdateView):
    model=Other
    fields = '__all__'
    template_name='deals/other/other_form_edit.html'

    def get(self, request, **kwargs):
        print(self.request.id)
        return self.request.id


    
        
class OtherDeleteView(DeleteView):
    model=Other
    fields = '__all__'
    success_url=reverse_lazy('dashboard:deals:otherlist') 
    template_name='deals/other/other_confirm_delete.html'

from .models import BankNew
from .forms import (SolicitorForm,AgentForm,ExecutorForm,FamilyForm,LiquidatorForm,
                    OtherForm,BankNewForm,SolicitorForm2,AgentForm2,BankNewForm2,ExecutorForm2,
                    FamilyForm2,LiquidatorForm2,OtherForm2)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

#SolicitorViews

def solicitor_list(request):
    context={}
    id=request.POST.get('id',0)
    # deal_id = request.Post.get()
    solicitors=Solicitor.objects.filter(created_by=str(request.user)).order_by('-id')
    select_list=solicitors

    if not id=="0" or 0:
        solicitors =solicitors.filter(id=id)
    context['solicitor_list']=solicitors
    context['select_list']=select_list
    return render(request,'deals/solicitor/solicitor_listing.html',context)

def solicitor_add(request):
    context={}
    # print(request.get_full_path())
    form =SolicitorForm(request.POST or None)
    
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        # deal = Deal.objects.get(lead_id=17)
        # myform.deal=myform
        # d_id = request.POST.get('d_id')
        # print(d_id)
        # myform.owner_id="1"
        # print(deal)
        # print("before save")
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/solicitor/solicitor_form.html',context)

def solicitor_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Solicitor.objects.get(pk=pk)
    form =SolicitorForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/solicitor/solicitor_form_edit.html',context)
# def get_queryset(self, *args, **kwargs):
#     return Deal.objects.filter(deal_id=self.kwargs['pk'])

def solicitor_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Solicitor.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/solicitor/solicitor_confirm_delete.html',context)

#AgentViews
def agent_list(request):
    context={}
    id=request.POST.get('id',0)
    agents=Agent.objects.filter(created_by=str(request.user)).order_by('-id')
    select_list=agents

    if not id=="0" or 0:
        agents =agents.filter(id=id)
    context['agent_list']=agents
    context['select_list']=select_list
    return render(request,'deals/agent/agent_listing.html',context)

def agent_add(request):
    context={}
   
    form =AgentForm(request.POST or None)
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        d_id = request.POST.get('d_id')
        # myform.owner_id="1"
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/agent/agent_form.html',context)

def agent_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Agent.objects.get(pk=pk)
    form =AgentForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/agent/agent_form_edit.html',context)

def agent_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Agent.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/agent/agent_confirm_delete.html',context)

# bankViews
def bank_list(request):
    context={}
    id=request.POST.get('id',0)
    # from leads.models import Bank
    banks=BankNew.objects.filter(created_by=str(request.user)).order_by('-id')
    print(banks)
    select_list=banks

    if not id=="0" or 0:
        banks =banks.filter(id=id)
    context['bank_list']=banks
    print(banks)
    context['select_list']=select_list
    return render(request,'deals/bank/bank_listing.html',context)

def bank_add(request):
    context={}
    form =BankNewForm(request.POST or None)
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        d_id = request.POST.get('d_id')
        # myform.owner_id="1"
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/bank/bank_form.html',context)

def bank_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =BankNew.objects.get(pk=pk)
    form =BankNewForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/bank/bank_form_edit.html',context)

def bank_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =BankNew.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/bank/bank_confirm_delete.html',context)


#executorViews
def executor_list(request):
    context={}
    id=request.POST.get('id',0)
    executors=Executor.objects.filter(created_by=str(request.user)).order_by('-id')
    select_list=executors

    if not id=="0" or 0:
        executors =executors.filter(id=id)
    context['executor_list']=executors
    context['select_list']=select_list
    return render(request,'deals/executor/executor_listing.html',context)

def executor_add(request):
    context={}
    form =ExecutorForm(request.POST or None)
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        d_id = request.POST.get('d_id')
        # myform.owner_id="1"
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/executor/executor_form.html',context)

def executor_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Executor.objects.get(pk=pk)
    form =ExecutorForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/executor/executor_form_edit.html',context)

def executor_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Executor.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/executor/executor_confirm_delete.html',context)

#familyViews
def family_list(request):
    context={}
    id=request.POST.get('id',0)
    familys=Family.objects.filter(created_by=str(request.user)).order_by('-id')
    select_list=familys

    if not id=="0" or 0:
        familys =familys.filter(id=id)
    context['family_list']=familys
    context['select_list']=select_list
    return render(request,'deals/family/family_listing.html',context)

def family_add(request):
    context={}
    form =FamilyForm(request.POST or None)
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        d_id = request.POST.get('d_id')
        # myform.owner_id="1"
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/family/family_form.html',context)

def family_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Family.objects.get(pk=pk)
    form =FamilyForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/family/family_form_edit.html',context)

def family_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Family.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/family/family_confirm_delete.html',context)

#liquidatorViews
def liquidator_list(request):
    context={}
    id=request.POST.get('id',0)
    liquidators=Liquidator.objects.filter(created_by=str(request.user)).order_by('-id')
    select_list=liquidators

    if not id=="0" or 0:
        liquidators =liquidators.filter(id=id)
    context['liquidator_list']=liquidators
    context['select_list']=select_list
    return render(request,'deals/liquidator/liquidator_listing.html',context)

def liquidator_add(request):
    context={}
    form =LiquidatorForm(request.POST or None)
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        d_id = request.POST.get('d_id')
        # myform.owner_id="1"
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/liquidator/liquidator_form.html',context)

def liquidator_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Liquidator.objects.get(pk=pk)
    form =LiquidatorForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/liquidator/liquidator_form_edit.html',context)

def liquidator_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Liquidator.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/liquidator/liquidator_confirm_delete.html',context)

#otherViews
def other_list(request):
    context={}
    id=request.POST.get('id',0)
    others=Other.objects.filter(created_by=str(request.user)).order_by('-id')
    select_list=others

    if not id=="0" or 0:
        others =others.filter(id=id)
    context['other_list']=others
    context['select_list']=select_list
    return render(request,'deals/other/other_listing.html',context)

def other_add(request):
    context={}
    form =OtherForm(request.POST or None)
    if form.is_valid():
        myform =form.save(commit=False)
        myform.created_by=str(request.user)
        d_id = request.POST.get('d_id')
        # myform.owner_id="1"
        myform.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/other/other_form.html',context)

def other_edit(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Other.objects.get(pk=pk)
    form =OtherForm2(request.POST or None, instance=s_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'success':"ok"})
    context['form']=form
    return render(request,'deals/other/other_form_edit.html',context)

def other_delete(request,pk=None):
    context={}
    context['pk']=pk
    s_obj =Other.objects.get(pk=pk)
    if request.method=="POST":
        s_obj.delete()
        return JsonResponse({'success':"ok"})
    return render(request,'deals/other/other_confirm_delete.html',context)

# class SolicitorView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         ctx = self.get_context_data(*args, **kwargs)
#         return render(request, "deals/solicitor/solicitor_listing.html", ctx)

#     def get_context_data(self, *args, **kwargs):
#         deal = Deal.objects.select_related("lead__user", "lead").get(
#             pk=kwargs["deal_id"]
#         )
#         if deal.lead.user != self.request.user:
#             raise Http404
#         solicitor = Solicitor.objects.filter(deal=deal)
#         if solicitor:
#             solicitor_form = SolicitorForm(
#                 instance=solicitor.first()
#             )
#         else:
#             solicitor_form = SolicitorForm()
#         ctx = {
#             "form": solicitor_form,
#             "lead_id": deal.lead.pk,
#             "deal_id": deal.pk,
#         }
#         return ctx

#     def get_success_url(self):
#         messages.success(
#             self.request,
#             "The details have been saved successfully!",
#             extra_tags="submitted",
#         )
#         return reverse_lazy(
#             "dashboard:deals:solicitorlisting",
#             kwargs={"deal_id": self.kwargs["deal_id"]},
#         )

#     def post(self, request, *args, **kwargs):
#         deal = Deal.objects.select_related("lead__user").get(
#             pk=kwargs["deal_id"]
#         )
#         if deal.lead.user != self.request.user:
#             raise Http404
#         solicitor = Solicitor.objects.filter(deal=deal)
#         if solicitor:
#             solicitor_form = SolicitorForm(
#                 request.POST, instance=Solicitor.first()
#             )
#         else:
#             solicitor_form = SolicitorForm(request.POST)
#         if solicitor_form.is_valid():
#             return self.form_valid(SolicitorForm)
#         else:
#             return self.form_invalid(SolicitorForm)

#     def form_valid(self, form):
#         deal = Deal.objects.get(pk=self.kwargs["deal_id"])
#         solicitor_obj = form.save(commit=False)
#         solicitor_obj.deal = deal
#         solicitor_obj.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form):
#         deal = Deal.objects.select_related("lead").get(
#             pk=self.kwargs["deal_id"]
#         )
#         ctx = {"form": form, "lead_id": deal.lead.pk, "deal_id": deal.pk}
#         return render(
#             self.request, "deals/solicitor/solicitor_listing.html", ctx
        # )




