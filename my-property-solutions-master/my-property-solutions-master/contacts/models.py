from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class PropertiesInspected(models.Model):
    contact = models.ForeignKey(
        "Contact", on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.CharField(
        _("Address"), max_length=100, null=True, blank=True
    )
    number_regex = RegexValidator(
        regex=r"^[\d\,]*$", message="Enter whole numbers."
    )
    inspection_costs = models.CharField(
        _("Inspection Costs"),
        validators=[number_regex],
        max_length=50,
        null=True,
        blank=True,
    )


class PropertiesEmployed(models.Model):
    contact = models.ForeignKey(
        "Contact", on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.CharField(
        _("Address"), max_length=100, null=True, blank=True
    )
    quote = models.IntegerField(_("Quote"), null=True, blank=True)
    number_regex = RegexValidator(
        regex=r"^[\d\,]*$", message="Enter whole numbers."
    )
    total = models.CharField(
        _("Total"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


class Contact(models.Model):
    """
    Will store the details of all kinds of contacts ex: painter, builder, lawyer, agents etc.
    """

    ABN_ACN_CHOICES = (("", "---------"), ("ABN", "ABN"), ("ACN", "ACN"))
    CONTACT_TYPE_CHOICES = (
        ("", "-----------"),
        ("Branch", "Branch"),
        ("Head Office", "Head Office"),
    )
    EXECUTOR_TYPE_CHOICES = (
        ("No Executor", "No Executor"),
        ("Lawyer", "Lawyer"),
        ("Relative", "Relative"),
    )
    STATUS_CHOICES = (("Yes", "Yes"), ("No", "No"))
    PAYMENT_TYPE_CHOICES = (
        ("Profit Split", "Profit Split"),
        ("Interest ROI", "Interest ROI"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    _property = models.ForeignKey(
        "leads.Property", on_delete=models.CASCADE, null=True, blank=True
    )
    lender = models.ForeignKey(
        "deals.MyPurchaseDetails",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_lender_details",
    )
    is_solicitor = models.CharField(
        _("Is There A Solicitor"),
        choices=STATUS_CHOICES,
        max_length=50,
        default="Yes",
        null=True,
        blank=True,
    )
    category = models.CharField(
        _("Category"), max_length=100, null=True, blank=True
    )
    sub_category = models.CharField(
        _("Sub Category"), max_length=100, null=True, blank=True
    )
    company = models.CharField(
        _("Company"), max_length=100, null=True, blank=True
    )
    abn_or_acn = models.CharField(
        _("ABN/ACN"),
        max_length=15,
        choices=ABN_ACN_CHOICES,
        default="ABN",
        null=True,
        blank=True,
    )
    abn_or_acn_number = models.IntegerField(
        _("ABN/ACN Number"), null=True, blank=True
    )
    contact_name = models.CharField(
        _("Contact Name"), max_length=100, null=True, blank=True
    )
    po_box = models.CharField(
        _("PO Box"), max_length=100, null=True, blank=True
    )
    postal_suburb = models.CharField(
        _("Suburb"), max_length=100, null=True, blank=True
    )
    postal_state = models.CharField(
        _("State"), max_length=100, null=True, blank=True
    )
    postal_post_code = models.CharField(
        _("Post Code"), max_length=100, null=True, blank=True
    )
    unit = models.CharField(_("Unit"), max_length=100, null=True, blank=True)
    number = models.IntegerField(_("Number"), null=True, blank=True)
    street = models.CharField(
        _("Street"), max_length=100, null=True, blank=True
    )
    suburb = models.CharField(
        _("Suburb"), max_length=100, null=True, blank=True
    )
    state = models.CharField(_("State"), max_length=100, null=True, blank=True)
    post_code = models.CharField(
        _("Post Code"), max_length=100, null=True, blank=True
    )
    mobile_regex = RegexValidator(
        regex=r"^[(\d) ]{10,15}$",
        message="Mobile number must be entered in the format: 'XXXXXXXXXX' or '(XX) XXXXXXXXXX'. Up to 12 digits allowed.",
    )
    mobile = models.CharField(
        validators=[mobile_regex], max_length=17, null=True, blank=True
    )  # validators should be a list
    office_phone_regex = RegexValidator(
        regex=r"^[(\d) ]{10,15}$",
        message="Phone number must be entered in the format: 'XXXXXXXXXX' or '(XX) XXXXXXXXXX'. Up to 12 digits allowed.",
    )
    office_phone = models.CharField(
        _("Office Phone"),
        validators=[office_phone_regex],
        max_length=17,
        null=True,
        blank=True,
    )
    office_fax = models.CharField(
        _("Office Fax"),
        validators=[office_phone_regex],
        max_length=100,
        null=True,
        blank=True,
    )
    email = models.EmailField(_("Email"), null=True, blank=True)
    contact_type = models.CharField(
        _("Type"),
        max_length=100,
        choices=CONTACT_TYPE_CHOICES,
        default="",
        null=True,
        blank=True,
    )
    number_regex = RegexValidator(
        regex=r"^[\d\,.]*$", message="Enter whole numbers."
    )
    trade_rating_regex = RegexValidator(
        regex=r"^[\d\/]*$", message="Enter rating in the format 10/10."
    )
    rate_per_hour = models.CharField(
        _("Rate/hour"), max_length=50, null=True, blank=True
    )
    trade_rating = models.CharField(
        _("Trade Rating"),
        max_length=50,
        validators=[trade_rating_regex],
        null=True,
        blank=True,
    )
    listed_price = models.CharField(
        _("Listed Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    reference = models.CharField(
        _("Reference"), max_length=100, null=True, blank=True
    )
    executor_type = models.CharField(
        _("Executor"),
        max_length=20,
        choices=EXECUTOR_TYPE_CHOICES,
        default="No Executor",
        null=True,
        blank=True,
    )  # Field for add-lead's form wizard
    website = models.CharField(
        _("Website"), max_length=50, null=True, blank=True
    )
    position = models.CharField(
        _("Position"), max_length=50, null=True, blank=True
    )
    license_number = models.CharField(
        _("License Number"), max_length=50, null=True, blank=True
    )
    insurance_cover_amount = models.CharField(
        _("Insurance Cover Amount"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    insurance_expiry = models.DateField(
        _("Insurance Expiry"), null=True, blank=True
    )
    industry_type = models.CharField(
        _("Industry Type"), max_length=50, null=True, blank=True
    )
    # These seven fields are being imported(moved) from deals/MyPurchaseDetails model
    investment_amount = models.CharField(
        _("Investment Amount"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    agreed_interest_rate_per_annum = models.DecimalField(
        _("Agreed Interest Rate (PA)"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    duration_in_months = models.IntegerField(
        _("Duration (Months)"), null=True, blank=True
    )
    roi_approx = models.CharField(
        _("ROI (Approx.)"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    total_approx = models.CharField(
        _("Total (Approx.)"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    # everytime before calculating the profit split, the payment_type has to be checked first and accordingly the share has to be calculated
    payment_type = models.CharField(
        _("Payment type"),
        choices=PAYMENT_TYPE_CHOICES,
        max_length=50,
        default="Interest ROI",
        null=True,
        blank=True,
    )
    profit_split = models.DecimalField(
        _("Profit Split (%)"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    is_agent = models.CharField(
        _("Is There An Agent"),
        choices=STATUS_CHOICES,
        max_length=50,
        default="Yes",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.contact_name:
            return self.contact_name
        else:
            return ""
