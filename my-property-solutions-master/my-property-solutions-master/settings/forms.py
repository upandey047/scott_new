from django import forms

from my_property_solutions.forms import FormFormatter
from .models import (
    Address,
    RegisteredAddress,
    Individual,
    Email,
    Company,
    Shares,
    Trust,
    Documents,
    Event,
    CheckList,
)


class AddressForm(FormFormatter):
    class Meta:
        model = Address
        exclude = ["individual", "company", "trust"]


# RegisteredAddressForm is only used for a company entity
class RegisteredAddressForm(FormFormatter):
    class Meta:
        model = RegisteredAddress
        exclude = ["company"]


class IndividualForm(FormFormatter):
    class Meta:
        model = Individual
        exclude = ["user", "address", "documents"]


class EmailForm(FormFormatter):
    class Meta:
        model = Email
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["required"] = True


EmailFormSet = forms.formset_factory(EmailForm, extra=1)
EditEmailFormSet = forms.modelformset_factory(
    Email, form=EmailForm, exclude=[], extra=0
)  # Formset for editing email


class CompanyForm(FormFormatter):
    class Meta:
        model = Company
        exclude = ["user", "documents", "gst_number"]


class SharesForm(FormFormatter):
    class Meta:
        model = Shares
        exclude = ["trust"]


SharesFormSet = forms.formset_factory(SharesForm, extra=1)
EditSharesFormSet = forms.modelformset_factory(
    Shares, form=SharesForm, exclude=["trust"], extra=0
)  # Formset for editing shares


class TrustForm(FormFormatter):
    class Meta:
        model = Trust
        exclude = ["user", "address", "documents"]


class DocumentsForm(FormFormatter):
    class Meta:
        model = Documents
        exclude = ["electronic_letterhead", "brochure"]


# Checklist forms
class AddOrEditEventToCheckListForm(FormFormatter):
    class Meta:
        model = Event
        exclude = ["default_event"]


class CheckListForm(FormFormatter):
    class Meta:
        exclude = ["category", "event"]
        model = CheckList

    def __init__(self, *args, **kwargs):
        super(CheckListForm, self).__init__(*args, **kwargs)
        self.fields["event"].widget.attrs["disabled"] = True


CheckListFormSet = forms.modelformset_factory(
    CheckList,
    form=CheckListForm,
    exclude=("user", "deal", "category"),
    extra=0,
)
