from django import forms
from django.forms import fields

from my_property_solutions.forms import FormFormatter
from .models import (
    Deal,
    Purchase,
    PurchaseCosts,
    Sale,
    ProfitSplit,
    PurchaseComparableSales,
    PurchaseComparableSalesImages,
    SaleComparableSales,
    SaleComparableSalesImages,
    Renovation,
    Team,
    Rooms,
    Tasks,
    Images,
    MyPurchaseDetails,
    Materials,
    PrimeCostItems,
    PurchaseCorrespondanceDocuments,
    External,
    ExternalTasks,
    ExternalMaterials,
    InternalTasksForMyself,
    ExternalTasksForMyself,
    HoldingCosts,
    FeasibilityReport,
    AFCAComplaintLodged,
    ListForSale,
    Sold,
    SaleDealInformation,
    BankNew
)
from leads.models import Bank



class DealOverviewForm(FormFormatter):
    class Meta:
        exclude = ["lead", "type"]
        model = Deal


class SaleDealInformationForm(FormFormatter):
    class Meta:
        exclude = ["deal"]
        model = SaleDealInformation


class PurchaseForm(FormFormatter):
    class Meta:
        exclude = []
        model = Purchase


class PurchaseCostsForm(FormFormatter):
    class Meta:
        exclude = ["purchase"]
        model = PurchaseCosts


PurchaseCostsFormset = forms.modelformset_factory(
    PurchaseCosts, form=PurchaseCostsForm, exclude=["purchase"], extra=0
)


class HoldingCostsForm(FormFormatter):
    class Meta:
        exclude = ["purchase"]
        model = HoldingCosts


HoldingCostsFormset = forms.modelformset_factory(
    HoldingCosts, form=HoldingCostsForm, exclude=["purchase"], extra=0
)


class PurchaseComparableSalesForm(FormFormatter):
    class Meta:
        exclude = ["purchase"]
        model = PurchaseComparableSales

    def __init__(self, *args, **kwargs):
        super(PurchaseComparableSalesForm, self).__init__(*args, **kwargs)
        self.fields["land"].help_text = "in sqm"
        self.fields["sale_date"].widget.attrs["autocomplete"] = "off"


class PurchaseComparableSalesImagesForm(FormFormatter):
    class Meta:
        exclude = ["comparable_sale"]
        model = PurchaseComparableSalesImages


PurchaseComparableSalesImagesFormset = forms.formset_factory(
    PurchaseComparableSalesImagesForm, extra=1
)
PurchaseComparableSalesImagesModelFormset = forms.modelformset_factory(
    PurchaseComparableSalesImages,
    form=PurchaseComparableSalesImagesForm,
    exclude=["comparable_sale"],
    extra=0,
)


class PurchaseFeasibilityReportForm(FormFormatter):
    class Meta:
        exclude = ["purchase"]
        model = FeasibilityReport


class SaleForm(FormFormatter):
    class Meta:
        exclude = []
        model = Sale


class ProfitSplitForm(FormFormatter):
    class Meta:
        fields = ["entity", "percentage", "amount"]
        model = ProfitSplit


ProfitSplitFormset = forms.formset_factory(ProfitSplitForm, extra=1)
ProfitSplitModelFormset = forms.modelformset_factory(
    ProfitSplit,
    form=ProfitSplitForm,
    fields=["entity", "percentage", "amount"],
    extra=0,
)


class SaleComparableSalesForm(FormFormatter):
    class Meta:
        exclude = ["sale"]
        model = SaleComparableSales

    def __init__(self, *args, **kwargs):
        super(SaleComparableSalesForm, self).__init__(*args, **kwargs)
        self.fields["land"].help_text = "in sqm"
        self.fields["sale_date"].widget.attrs["autocomplete"] = "off"


class SaleComparableSalesImagesForm(FormFormatter):
    class Meta:
        exclude = ["comparable_sale"]
        model = SaleComparableSalesImages


SaleComparableSalesImagesFormset = forms.formset_factory(
    SaleComparableSalesImagesForm, extra=1
)
SaleComparableSalesImagesModelFormset = forms.modelformset_factory(
    SaleComparableSalesImages,
    form=SaleComparableSalesImagesForm,
    exclude=["comparable_sale"],
    extra=0,
)


class RenovationForm(FormFormatter):
    class Meta:
        exclude = ["purchase", "current_expenses"]
        model = Renovation

    def __init__(self, *args, **kwargs):
        super(RenovationForm, self).__init__(*args, **kwargs)
        self.fields["renovation_difference"].widget.attrs["readonly"] = True


class TeamForm(FormFormatter):
    class Meta:
        exclude = ["renovation"]
        model = Team


class SearchContactForm(forms.Form):
    search_contact = forms.CharField(label="Search", max_length=100)
    search_contact_id = forms.CharField(
        label="Search Id", max_length=10, required=False
    )

    def __init__(self, *args, **kwargs):
        super(SearchContactForm, self).__init__(*args, **kwargs)
        self.fields["search_contact"].widget.attrs["class"] = "form-control"
        self.fields["search_contact"].widget.attrs[
            "placeholder"
        ] = "Enter Contact Categories"
        self.fields["search_contact"].widget.attrs["autocomplete"] = "off"


class RoomsDetailsForm(FormFormatter):
    class Meta:
        exclude = [
            "renovation",
            "parking",
            "entry",
            "lounge",
            "dining",
            "kitchen",
            "laundry",
            "bathroom",
            "bedroom",
            "room_difference",
            "room_total_cost",
        ]
        model = Rooms
        widgets = {
            "room_thoughts": forms.Textarea(attrs={"cols": 80, "rows": 3})
        }

    def __init__(self, *args, **kwargs):
        super(RoomsDetailsForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].widget.attrs["autocomplete"] = "off"
        self.fields["completion_date"].widget.attrs["autocomplete"] = "off"


class RoomsForm(FormFormatter):
    class Meta:
        exclude = [
            "renovation",
            "parking",
            "entry",
            "lounge",
            "dining",
            "kitchen",
            "laundry",
            "bathroom",
            "bedroom",
            "room_difference",
            "room_total_cost",
            "thoughts",
        ]
        model = Rooms

    def __init__(self, *args, **kwargs):
        super(RoomsForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].widget.attrs["autocomplete"] = "off"
        self.fields["completion_date"].widget.attrs["autocomplete"] = "off"


class TasksForm(FormFormatter):
    class Meta:
        exclude = ["room", "service_man"]
        model = Tasks

    def __init__(self, *args, **kwargs):
        super(TasksForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs["class"] = ""


TasksFormset = forms.formset_factory(TasksForm, extra=1)
TasksModelFormset = forms.modelformset_factory(
    Tasks, form=TasksForm, exclude=["room", "service_man"], extra=0
)


class ImagesForm(FormFormatter):
    class Meta:
        exclude = ["renovation", "category"]
        model = Images


ImagesFormset = forms.formset_factory(ImagesForm, extra=1)
ImagesModelFormset = forms.modelformset_factory(
    Images, form=ImagesForm, exclude=["renovation", "category"], extra=0
)


class MyPurchaseDetailsForm(FormFormatter):
    class Meta:
        exclude = ["purchase"]
        model = MyPurchaseDetails


class MyBankDetailsForm(FormFormatter):
    class Meta:
        exclude = ["mortgaged", "current_amount", "arrears"]
        model = Bank


class MaterialsForm(FormFormatter):
    class Meta:
        exclude = ["room"]
        model = Materials


MaterialsFormset = forms.formset_factory(MaterialsForm, extra=1)
MaterialsModelFormset = forms.modelformset_factory(
    Materials, form=MaterialsForm, exclude=["room"], extra=0
)


class PrimeCostItemsForm(FormFormatter):
    class Meta:
        exclude = ["room"]
        model = PrimeCostItems


PrimeCostItemsFormset = forms.modelformset_factory(
    PrimeCostItems, form=PrimeCostItemsForm, exclude=["room"], extra=0
)


class PurchaseCorrespondanceDocumentsForm(FormFormatter):
    class Meta:
        exclude = ["purchase"]
        model = PurchaseCorrespondanceDocuments

    def __init__(self, *args, **kwargs):
        super(PurchaseCorrespondanceDocumentsForm, self).__init__(
            *args, **kwargs
        )
        self.fields["document"].required = True


PurchaseCorrespondanceDocumentsFormset = forms.formset_factory(
    PurchaseCorrespondanceDocumentsForm, extra=1
)
PurchaseCorrespondanceDocumentsModelFormset = forms.modelformset_factory(
    PurchaseCorrespondanceDocuments,
    form=PurchaseCorrespondanceDocumentsForm,
    exclude=["purchase"],
    extra=0,
)


class ExternalLocationForm(FormFormatter):
    class Meta:
        fields = ["location"]
        model = External

    def __init__(self, *args, **kwargs):
        super(ExternalLocationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["use_required_attribute"] = True
            field.widget.attrs["required"] = True


ExternalLocationFormset = forms.formset_factory(ExternalLocationForm, extra=1)
ExternalLocationModelFormset = forms.modelformset_factory(
    External, form=ExternalLocationForm, fields=["location"], extra=0
)


class ExternalForm(FormFormatter):
    class Meta:
        exclude = ["renovation", "difference", "thoughts", "total_cost"]
        model = External

    def __init__(self, *args, **kwargs):
        super(ExternalForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].widget.attrs["autocomplete"] = "off"
        self.fields["completion_date"].widget.attrs["autocomplete"] = "off"


class ExternalDetailsForm(FormFormatter):
    class Meta:
        exclude = ["renovation", "total_cost", "difference"]
        model = External
        widgets = {"thoughts": forms.Textarea(attrs={"cols": 80, "rows": 3})}

    def __init__(self, *args, **kwargs):
        super(ExternalDetailsForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].widget.attrs["autocomplete"] = "off"
        self.fields["completion_date"].widget.attrs["autocomplete"] = "off"


class ExternalTasksForm(FormFormatter):
    class Meta:
        exclude = ["location", "service_man"]
        model = ExternalTasks

    def __init__(self, *args, **kwargs):
        super(ExternalTasksForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs["class"] = ""


ExternalTasksFormset = forms.formset_factory(ExternalTasksForm, extra=1)
ExternalTasksModelFormset = forms.modelformset_factory(
    ExternalTasks, form=TasksForm, exclude=["room", "service_man"], extra=0
)


class ExternalMaterialsForm(FormFormatter):
    class Meta:
        exclude = ["location"]
        model = ExternalMaterials


ExternalMaterialsFormset = forms.formset_factory(
    ExternalMaterialsForm, extra=1
)
ExternalMaterialsModelFormset = forms.modelformset_factory(
    ExternalMaterials,
    form=ExternalMaterialsForm,
    exclude=["location"],
    extra=0,
)


class ExternalTasksForMyselfForm(forms.ModelForm):
    class Meta:
        exclude = ["location"]
        model = ExternalTasksForMyself

    def __init__(self, *args, **kwargs):
        super(ExternalTasksForMyselfForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = field.label
        self.fields["task_name"].widget.attrs["class"] = "form-control"


ExternalTasksForMyselfFormset = forms.formset_factory(
    ExternalTasksForMyselfForm, extra=1
)
ExternalTasksForMyselfModelFormset = forms.modelformset_factory(
    ExternalTasksForMyself,
    form=ExternalTasksForMyselfForm,
    exclude=["location"],
    extra=0,
)


class InternalTasksForMyselfForm(forms.ModelForm):
    class Meta:
        exclude = ["room"]
        model = InternalTasksForMyself

    def __init__(self, *args, **kwargs):
        super(InternalTasksForMyselfForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = field.label
        self.fields["task_name"].widget.attrs["class"] = "form-control"


InternalTasksForMyselfFormset = forms.formset_factory(
    InternalTasksForMyselfForm, extra=1
)
InternalTasksForMyselfModelFormset = forms.modelformset_factory(
    InternalTasksForMyself,
    form=InternalTasksForMyselfForm,
    exclude=["room"],
    extra=0,
)


class AFCAComplaintLodgedForm(FormFormatter):
    class Meta:
        exclude = ["deal"]
        model = AFCAComplaintLodged
        widgets = {"comments": forms.Textarea(attrs={"cols": 80, "rows": 2})}


class ListForSaleForm(FormFormatter):
    class Meta:
        exclude = ["deal"]
        model = ListForSale


class SoldForm(FormFormatter):
    class Meta:
        exclude = ["deal"]
        model = Sold

from .models import Solicitor,Agent,Executor,Liquidator,Family,Other
class SolicitorForm(forms.ModelForm):
    class Meta:
        model =Solicitor
        exclude=("created_by",)
        
class AgentForm(forms.ModelForm):
    class Meta:
        model =Agent
        exclude=("created_by",)
        
class BankNewForm(forms.ModelForm):
    class Meta:
        model =BankNew
        exclude=("created_by",)
        # fields=['bank','unit','office_phone','email']
        # labels = {
        #     'unit': 'Postal Address'        
        # }
        
class ExecutorForm(forms.ModelForm):
    class Meta:
        model =Executor
        exclude=("created_by",)
        
class FamilyForm(forms.ModelForm):
    class Meta:
        model =Family
        exclude=("created_by",)
        
class LiquidatorForm(forms.ModelForm):
    class Meta:
        model =Liquidator
        exclude=("created_by",)
        
class OtherForm(forms.ModelForm):
    class Meta:
        model =Other
        exclude=("created_by",)

        

