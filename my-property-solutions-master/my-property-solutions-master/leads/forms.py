from django import forms

from my_property_solutions.forms import FormFormatter
from .models import (
    PropertyOwner,
    Property,
    Bank,
    LandDetails,
    Zoning,
    Shape,
    StreetAppeal,
    Construction,
    Parking,
    Features,
    GrannyFlat,
    Entry,
    Lounge,
    Dining,
    Kitchen,
    Laundry,
    Bathroom,
    Bedroom,
    PersonalLoan,
    Title,
    Dealing,
    Auction,
    Lead,
)
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _


class PropertyOwnerForm(FormFormatter):
    class Meta:
        fields = ["first_name", "last_name", "email", "mobile"]
        model = PropertyOwner

    def __init__(self, *args, **kwargs):
        super(PropertyOwnerForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["required"] = False
        self.fields["last_name"].widget.attrs["required"] = False


class DeceasedPropertyOwnerForm(FormFormatter):
    class Meta:
        fields = ["first_name", "last_name"]
        model = PropertyOwner

    def __init__(self, *args, **kwargs):
        super(DeceasedPropertyOwnerForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["required"] = True
        self.fields["last_name"].widget.attrs["required"] = True


class BankruptcyPropertyOwnerForm(FormFormatter):
    class Meta:
        fields = [
            "company_name",
            "abn_or_acn",
            "abn_or_acn_number",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "po_box",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
        ]
        model = PropertyOwner

    def __init__(self, *args, **kwargs):
        super(BankruptcyPropertyOwnerForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["required"] = True
        self.fields["last_name"].widget.attrs["required"] = True


class PropertyForm(FormFormatter):
    class Meta:
        exclude = [
            "lead",
            "original_list_date",
            "todays_date",
            "on_or_off_market",
            "start_list_price",
            "end_list_price",
            "start_list_date",
            "end_list_date",
            "difference",
            "dom",
        ]
        model = Property

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields["land"].help_text = "in sqm"


class DeceasedPropertyForm(FormFormatter):
    class Meta:
        exclude = [
            "lead",
            "original_list_date",
            "todays_date",
            "on_or_off_market",
            "start_list_price",
            "end_list_price",
            "start_list_date",
            "end_list_date",
            "difference",
            "dom",
        ]
        model = Property

    def __init__(self, *args, **kwargs):
        super(DeceasedPropertyForm, self).__init__(*args, **kwargs)
        self.fields["land"].help_text = "in sqm"


class DivorcePropertyForm(FormFormatter):
    class Meta:
        exclude = [
            "lead",
            "original_list_date",
            "todays_date",
            "on_or_off_market",
            "start_list_price",
            "end_list_price",
            "start_list_date",
            "end_list_date",
            "difference",
            "dom",
        ]
        model = Property

    def __init__(self, *args, **kwargs):
        super(DivorcePropertyForm, self).__init__(*args, **kwargs)
        self.fields["land"].help_text = "in sqm"


class PropertyAddressForm(FormFormatter):
    class Meta:
        exclude = [
            "lead",
            "original_list_date",
            "todays_date",
            "on_or_off_market",
            "start_list_price",
            "end_list_price",
            "start_list_date",
            "end_list_date",
            "difference",
            "dom",
            "beds",
            "bath",
            "land",
            "garage",
        ]
        model = Property


class WithdrawnPropertyForm(FormFormatter):
    """
    This form will be used for the property form of withdrawn category because it contains some
    additonal paramters
    """

    class Meta:
        exclude = [
            "lead",
            "original_list_date",
            "todays_date",
            "on_or_off_market",
            "start_list_price" "end_list_price",
        ]
        model = Property

    def __init__(self, *args, **kwargs):
        super(WithdrawnPropertyForm, self).__init__(*args, **kwargs)
        self.fields["land"].help_text = "in sqm"


class AdditionalPropertyDetailsForm(FormFormatter):
    """
    This form will be used for the property form of withdrawn category because it contains some
    additonal paramters
    """

    class Meta:
        fields = [
            "start_list_date",
            "end_list_date",
            "start_list_price",
            "end_list_price",
            "difference",
            "dom",
        ]
        model = Property


class BankForm(FormFormatter):
    class Meta:
        exclude = ["current_amount", "arrears"]
        model = Bank


class AuctionForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = Auction


class NotSheriffAuctionForm(FormFormatter):
    class Meta:
        exclude = ["_property", "deposit_required", "days"]
        model = Auction


PropertyOwnerModelFormset = modelformset_factory(
    PropertyOwner, form=PropertyOwnerForm, exclude=["_property"], extra=0
)
PropertyOwnerFormset = formset_factory(PropertyOwnerForm, extra=1)
BankruptcyPropertyOwnerFormset = formset_factory(
    BankruptcyPropertyOwnerForm, extra=1
)
BankruptcyPropertyOwnerModelFormset = modelformset_factory(
    PropertyOwner,
    form=BankruptcyPropertyOwnerForm,
    exclude=["_property"],
    extra=0,
)
DeceasedPropertyOwnerFormset = formset_factory(
    DeceasedPropertyOwnerForm, extra=1
)
DeceasedPropertyOwnerModelFormset = modelformset_factory(
    PropertyOwner,
    form=DeceasedPropertyOwnerForm,
    exclude=["_property"],
    extra=0,
)


# Inspection Sheet forms
class LandDetailsForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = LandDetails
        help_texts = {"dp_or_sp": _("For ex: DP 1234 or SP 1234")}


class ZoningForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = Zoning


class ShapeForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = Shape


class StreetAppealForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = StreetAppeal
        widgets = {
            "street_appeal_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            )
        }


class ConstructionForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = Construction
        widgets = {
            "foundation_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "external_walls_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "roof_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
        }


class ParkingForm(FormFormatter):
    class Meta:
        exclude = ["_property", "location_name"]
        model = Parking
        widgets = {
            "parking_comments": forms.Textarea(attrs={"cols": 80, "rows": 2})
        }


class FeaturesForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = Features
        widgets = {
            "pool_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "fencing_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "deck_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "retaining_walls_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FeaturesForm, self).__init__(*args, **kwargs)
        self.fields["pool_material"].required = False
        self.fields["pool_condition"].required = False
        self.fields["registerd"].required = False
        self.fields["retaining_walls_condition"].required = False
        self.fields["deck_condition"].required = False
        self.fields["deck_material"].required = False


class GrannyFlatForm(FormFormatter):
    class Meta:
        exclude = ["_property"]
        model = GrannyFlat
        widgets = {
            "granny_foundation_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "granny_walls_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "granny_roof_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GrannyFlatForm, self).__init__(*args, **kwargs)
        self.fields["granny_foundation_condition"].required = False
        self.fields["granny_walls_condition"].required = False
        self.fields["granny_roof_condition"].required = False
        self.fields["granny_foundation_description"].required = False
        self.fields["granny_walls_description"].required = False
        self.fields["granny_roof_description"].required = False


# Internal Details Forms
class EntryForm(FormFormatter):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Entry
        widgets = {
            "floors_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "ceiling_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "walls_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "light_fittings_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "curtains_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields["floors_condition"].required = False
        self.fields["ceiling_condition"].required = False
        self.fields["walls_condition"].required = False


EntryModelFormset = modelformset_factory(
    Entry, form=EntryForm, exclude=["_property", "granny_flat"], extra=0
)


class LoungeForm(forms.ModelForm):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Lounge
        widgets = {
            "floors_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "ceiling_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "walls_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "light_fittings_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "curtains_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super(LoungeForm, self).__init__(*args, **kwargs)
        count = (
            0
        )  # The fields for features are not required to have a placeholder and class form-control
        for field_name, field in self.fields.items():
            if count == 28:
                break
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            count = count + 1
        self.fields["floors_condition"].required = False
        self.fields["ceiling_condition"].required = False
        self.fields["walls_condition"].required = False


LoungeModelFormset = modelformset_factory(
    Lounge, form=LoungeForm, exclude=["_property", "granny_flat"], extra=0
)


class DiningForm(forms.ModelForm):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Dining
        widgets = {
            "floors_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "ceiling_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "walls_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "light_fittings_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "curtains_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super(DiningForm, self).__init__(*args, **kwargs)
        count = (
            0
        )  # The fields for features are not required to have a placeholder and class form-control
        for field_name, field in self.fields.items():
            if count == 28:
                break
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            count = count + 1
        self.fields["floors_condition"].required = False
        self.fields["ceiling_condition"].required = False
        self.fields["walls_condition"].required = False


DiningModelFormset = modelformset_factory(
    Dining, form=DiningForm, exclude=["_property", "granny_flat"], extra=0
)


class KitchenForm(forms.ModelForm):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Kitchen
        widgets = {
            "sink_comments": forms.Textarea(attrs={"cols": 80, "rows": 2})
        }

    def __init__(self, *args, **kwargs):
        super(KitchenForm, self).__init__(*args, **kwargs)
        count = (
            0
        )  # The fields for features are not required to have a placeholder and class form-control
        for field_name, field in self.fields.items():
            if count == 13:
                break
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            count = count + 1


class LaundryForm(FormFormatter):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Laundry
        widgets = {
            "laundry_comments": forms.Textarea(attrs={"cols": 80, "rows": 2})
        }


class BathroomForm(FormFormatter):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Bathroom
        widgets = {
            "bathroom_comments": forms.Textarea(attrs={"cols": 80, "rows": 2})
        }


BathroomModelFormset = modelformset_factory(
    Bathroom, form=BathroomForm, exclude=["_property", "granny_flat"], extra=0
)


class BedroomForm(forms.ModelForm):
    class Meta:
        exclude = ["_property", "granny_flat"]
        model = Bedroom
        widgets = {
            "floors_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "ceiling_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "walls_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
            "light_fittings_comments": forms.Textarea(
                attrs={"cols": 80, "rows": 2}
            ),
            "curtains_comments": forms.Textarea(attrs={"cols": 80, "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super(BedroomForm, self).__init__(*args, **kwargs)
        count = (
            0
        )  # The fields for features are not required to have a placeholder and class form-control
        for field_name, field in self.fields.items():
            if count == 28:
                break
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            count = count + 1
        self.fields["floors_condition"].required = False
        self.fields["ceiling_condition"].required = False
        self.fields["walls_condition"].required = False


BedroomModelFormset = modelformset_factory(
    Bedroom, form=BedroomForm, exclude=["_property", "granny_flat"], extra=0
)


class PersonalLoanForm(FormFormatter):
    class Meta:
        exclude = ["lead"]
        model = PersonalLoan


PersonalLoanFormset = formset_factory(PersonalLoanForm, extra=1)
PersonalLoanModelFormset = modelformset_factory(
    PersonalLoan, form=PersonalLoanForm, exclude=["lead"], extra=0
)


class TitleForm(FormFormatter):
    class Meta:
        exclude = ["lead"]
        model = Title


TitleFormset = formset_factory(TitleForm, extra=1)
TitleModelFormset = modelformset_factory(
    Title, form=TitleForm, exclude=["lead"], extra=0
)


class DealingForm(FormFormatter):
    class Meta:
        exclude = ["lead"]
        model = Dealing


DealingFormset = formset_factory(DealingForm, extra=1)
DealingModelFormset = modelformset_factory(
    Dealing, form=DealingForm, exclude=["lead"], extra=0
)


class LeadStatusForm(FormFormatter):
    class Meta:
        fields = ["status"]
        model = Lead


class NewLeadForm(FormFormatter):
    class Meta:
        model = Lead
        fields = ["status", "category", "note"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].required = True


def _validate_data_is_positive(data):
    try:
        data = int(data)
    except TypeError:
        pass
    else:
        if data >= 0:
            return data
    raise forms.ValidationError("A positive whole number is required")


class NewPropertyForm(FormFormatter):
    class Meta:
        model = Property
        fields = [
            "property_type",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "beds",
            "bath",
            "garage",
            "land",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["number", "street", "suburb", "state", "post_code"]:
            self.fields[field_name].required = True

    def clean_beds(self):
        return _validate_data_is_positive(self.cleaned_data["beds"])

    def clean_bath(self):
        return _validate_data_is_positive(self.cleaned_data["bath"])

    def clean_garage(self):
        return _validate_data_is_positive(self.cleaned_data["garage"])

    def clean_land(self):
        return _validate_data_is_positive(self.cleaned_data["land"])


class NewPropertyOwnerForm(FormFormatter):
    class Meta:
        model = PropertyOwner
        fields = ["first_name", "last_name"]
