from my_property_solutions.forms import FormFormatter
from .models import Contact, PropertiesInspected, PropertiesEmployed
from django.forms import formset_factory, modelformset_factory


class CertifiersOrInspectorsForm(FormFormatter):
    class Meta:
        model = Contact
        fields='__all__'
        # exclude = [
            # "company",
            # "abn_or_acn",
            # "abn_or_acn_number",
            # "contact_name",
            # "po_box",
            # "postal_suburb",
            # "postal_state",
            # "postal_post_code",
            # "unit",
            # "number",
            # "street",
            # "suburb",
            # "state",
            # "post_code",
            # "mobile",
            # "office_phone",
            # "office_fax",
            # "email",
            # "rate_per_hour",
            # "trade_rating",
            # "website",
            # "position",
            # "license_number",
            # "insurance_cover_amount",
            # "insurance_expiry",
            # "industry_type",
        # ]


class PropertiesInspectedForm(FormFormatter):
    class Meta:
        exclude = ["contact"]
        model = PropertiesInspected


PropertiesInspectedFormSet = formset_factory(PropertiesInspectedForm, extra=1)
PropertiesInspectedModelFormSet = modelformset_factory(
    PropertiesInspected,
    form=PropertiesInspectedForm,
    exclude=["contact"],
    extra=0,
)


class ConstructionOrTradeForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "trade_rating",
            "website",
            "position",
            "license_number",
            "insurance_cover_amount",
            "insurance_expiry",
            "industry_type",
        ]


class PropertiesEmployedForm(FormFormatter):
    class Meta:
        exclude = ["contact"]
        model = PropertiesEmployed


PropertiesEmployedFormSet = formset_factory(PropertiesEmployedForm, extra=1)
PropertiesEmployedModelFormSet = modelformset_factory(
    PropertiesEmployed,
    form=PropertiesEmployedForm,
    exclude=["contact"],
    extra=0,
)


class DesignForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "website",
            "industry_type",
        ]


class DevelopersForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "trade_rating",
            "website",
            "industry_type",
        ]


class FinanceForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "contact_type",
            "rate_per_hour",
            "website",
            "industry_type",
        ]


class SurveyorsForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "trade_rating",
            "website",
            "industry_type",
        ]


class LegalForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "reference",
            "website",
            "industry_type",
        ]


class SolicitorForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "is_solicitor",
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "listed_price",
            "reference",
            "website",
        ]


SolicitorFormSet = formset_factory(SolicitorForm, extra=2)
SolicitorModelFormSet = modelformset_factory(
    Contact,
    form=SolicitorForm,
    fields=[
        "is_solicitor",
        "company",
        "abn_or_acn",
        "abn_or_acn_number",
        "contact_name",
        "po_box",
        "postal_suburb",
        "postal_state",
        "postal_post_code",
        "unit",
        "number",
        "street",
        "suburb",
        "state",
        "post_code",
        "mobile",
        "office_phone",
        "office_fax",
        "email",
        "rate_per_hour",
        "listed_price",
        "reference",
        "website",
        "investment_amount",
    ],
    extra=1,
)


class RealEstateContactForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "listed_price",
            "website",
            "industry_type",
        ]


class RealEstateForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "listed_price",
            "executor_type",
            "website",
            "industry_type",
            "is_agent",
        ]

    def __init__(self, *args, **kwargs):
        super(RealEstateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if field_name == "executor_type":
                field.widget.attrs["class"] += "field_executor_type"
            if field_name == "company":
                field.widget.attrs["class"] += "field_company"
            if field_name == "abn_or_acn":
                field.widget.attrs["class"] += "field_abn_or_acn"
            if field_name == "abn_or_acn_number":
                field.widget.attrs["class"] += "field_abn_or_acn_number"


RealEstateModelFormset = modelformset_factory(
    Contact,
    form=RealEstateForm,
    fields=[
        "company",
        "abn_or_acn",
        "abn_or_acn_number",
        "contact_name",
        "po_box",
        "postal_suburb",
        "postal_state",
        "postal_post_code",
        "unit",
        "number",
        "street",
        "suburb",
        "state",
        "post_code",
        "mobile",
        "office_phone",
        "office_fax",
        "email",
        "rate_per_hour",
        "listed_price",
        "executor_type",
        "website",
        "industry_type",
    ],
    extra=0,
)
RealEstateFormset = formset_factory(RealEstateForm, extra=1)


class RealEstateWithoutMarketForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "listed_price",
            "executor_type",
            "website",
            "industry_type",
        ]

    def __init__(self, *args, **kwargs):
        super(RealEstateWithoutMarketForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if field_name == "executor_type":
                field.widget.attrs["class"] += "field_executor_type"
            if field_name == "company":
                field.widget.attrs["class"] += "field_company"
            if field_name == "abn_or_acn":
                field.widget.attrs["class"] += "field_abn_or_acn"
            if field_name == "abn_or_acn_number":
                field.widget.attrs["class"] += "field_abn_or_acn_number"


class RealEstateFormDivorce(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "listed_price",
            "website",
            "industry_type",
        ]

    def __init__(self, *args, **kwargs):
        super(RealEstateFormDivorce, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if field_name == "company":
                field.widget.attrs["class"] += "field_company"
            if field_name == "abn_or_acn":
                field.widget.attrs["class"] += "field_abn_or_acn"
            if field_name == "abn_or_acn_number":
                field.widget.attrs["class"] += "field_abn_or_acn_number"


class CouncilContactForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "trade_rating",
            "website",
            "position",
            "license_number",
            "insurance_cover_amount",
            "insurance_expiry",
            "industry_type",
        ]


class OthersForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "company",
            "abn_or_acn",
            "abn_or_acn_number",
            "contact_name",
            "po_box",
            "postal_suburb",
            "postal_state",
            "postal_post_code",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "office_phone",
            "office_fax",
            "email",
            "rate_per_hour",
            "trade_rating",
            "website",
            "position",
            "license_number",
            "insurance_cover_amount",
            "insurance_expiry",
            "industry_type",
        ]


class PrivateLenderForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "investment_amount",
            "agreed_interest_rate_per_annum",
            "duration_in_months",
            "roi_approx",
            "total_approx",
            "payment_type",
            "profit_split",
        ]

    def __init__(self, *args, **kwargs):
        super(PrivateLenderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in [
                "investment_amount",
                "agreed_interest_rate_per_annum",
                "duration_in_months",
                "roi_approx",
                "total_approx",
            ]:
                field.widget.attrs["class"] += "interest_roi_field"
            else:
                field.widget.attrs["class"] += "".join(
                    str(field_name).lower().split(" ")
                )


class CouncilForm(FormFormatter):
    class Meta:
        model = Contact
        fields = [
            "po_box",
            "unit",
            "number",
            "street",
            "suburb",
            "state",
            "post_code",
            "mobile",
            "email",
        ]
