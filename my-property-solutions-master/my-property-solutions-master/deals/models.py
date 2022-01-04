from django.core.exceptions import ValidationError
from leads.models import PropertyOwner
from django.http import HttpResponse
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.core.validators import RegexValidator
from contacts.models import Contact
from django.urls import reverse
# from django.core.validators import MaxValueValidator, MinValueValidator
from leads.models import (
    Lead,
    Parking,
    Entry,
    Lounge,
    Dining,
    Kitchen,
    Laundry,
    Bathroom,
    Bedroom,
    Bank,
)

number_regex = RegexValidator(
    regex=r"^[\d\,]*(\.\d{1,2})?$",
    message="Enter a valid positive monetary value with or without two decimals.",
)


# Model for deal card for each new lead
class Deal(models.Model):
    """
    The additional details are for purchase deal info
    """
    TYPE_CHOICES = (("WS", "WS"), ("SS", "SS"), ("TO", "TO"))
    lead = models.OneToOneField(
        Lead, on_delete=models.CASCADE, null=True, blank=True
    )
    type = models.CharField(
        _("Deal Type"), choices=TYPE_CHOICES, max_length=5, default="WS"
    )
    exchange = models.DateField(_("Exchange Date"), null=True, blank=True)
    settlement = models.DateField(_("Settlement Date"), null=True, blank=True)
    cool_off_period_expires = models.DateField(
        _("Cool Off Period Expires"), null=True, blank=True
    )
    purchase_price = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    renovation_cost = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )


class SaleDealInformation(models.Model):
    """
    This model will be used to store the sale deal information via the deal overview page
    """

    deal = models.OneToOneField(
        Deal, on_delete=models.CASCADE, null=True, blank=True
    )
    exchange = models.DateField(_("Exchange Date"), null=True, blank=True)
    settlement = models.DateField(_("Settlement Date"), null=True, blank=True)
    cool_off_period_expires = models.DateField(
        _("Cool Off Period Expires"), null=True, blank=True
    )
    sale_price = models.CharField(
        _("Sale Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    commission_paid = models.CharField(
        _("Commission Paid"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


# Offer Details Models
class Purchase(models.Model):
    RENOVATION_CHOICES = (("Yes", "Yes"), ("No", "No"))
    deal = models.OneToOneField(
        Deal,
        on_delete=models.CASCADE,
        related_name="purchase",
        null=True,
        blank=True,
    )
    market_value = models.CharField(
        validators=[number_regex], max_length=50, null=True, blank=True
    )  # validators should be a list
    renovation_required = models.CharField(
        _("Renovation Required"),
        choices=RENOVATION_CHOICES,
        max_length=5,
        default="Yes",
    )
    renovation_allowance = models.CharField(
        _("Renovation Allowance"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    minimum_profit = models.CharField(
        _("Minimum Profit"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    total_purchase_costs = models.CharField(
        _("Total Purchase Costs"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    negative_regex = RegexValidator(
        regex=r"^([\d\,\-]+(\.00)?)?$", message="Enter Integer numbers."
    )
    maximum_offer = models.CharField(
        _("Maximum Offer"),
        max_length=50,
        validators=[negative_regex],
        null=True,
        blank=True,
    )


class PurchaseCosts(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(_("Cost Name"), max_length=50)
    amount = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )

    def __str__(self):
        return str(self.name)


class HoldingCosts(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(_("Cost Name"), max_length=50)
    amount = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )

    def __str__(self):
        return str(self.name)


class FeasibilityReport(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, null=True, blank=True
    )
    purchase_price = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    purchase_costs = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    renovation_costs = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    holding_costs = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    estimated_selling_price_lower_limit = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    estimated_selling_price_upper_limit = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    potential_profit_lower_limit = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    potential_profit_upper_limit = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    money_partner = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    net_profit_lower_limit = models.CharField(
        _("Net Profit Lower Limit"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    net_profit_upper_limit = models.CharField(
        _("Net Profit Upper Limit"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    comments = models.CharField(
        _("Comments"), max_length=100, null=True, blank=True
    )


class Sale(models.Model):
    deal = models.OneToOneField(
        Deal,
        on_delete=models.CASCADE,
        related_name="sale",
        null=True,
        blank=True,
    )
    sale_price = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    negative_regex = RegexValidator(
        regex=r"^[\d\,\-]*$", message="Enter Integer numbers."
    )
    capital_gain_gross = models.CharField(
        max_length=50, validators=[negative_regex], null=True, blank=True
    )
    agent_fees = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    mortgage_payout_figure = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    legal_fees = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    dealing_or_withdrawal_fees = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    council = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    strata_fees = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    additional_cost = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    additional_cost_comments = models.CharField(
        _("Comments"), max_length=100, null=True, blank=True
    )
    total_sale_costs = models.CharField(
        _("Total Sale Costs"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


class ProfitSplit(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, null=True, blank=True
    )
    entity = models.ForeignKey(
        "settings.entity", on_delete=models.CASCADE, null=True, blank=True
    )
    percentage = models.IntegerField(null=True, blank=True)
    negative_regex = RegexValidator(
        regex=r"^[\d\,\-\.]*$", message="Enter Integer numbers."
    )
    amount = models.CharField(
        max_length=50, validators=[negative_regex], null=True, blank=True
    )


class PurchaseComparableSales(models.Model):
    CHOICES = (
        ("Inferior", "Inferior"),
        ("Comparable", "Comparable"),
        ("Superior", "Superior"),
    )
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="comparable_sales",
        null=True,
        blank=True,
    )
    address = models.CharField(
        _("Address"), max_length=200, null=True, blank=True
    )
    beds = models.IntegerField(_("Beds"), default=0)
    bath = models.IntegerField(_("Bath"), default=0)
    land = models.IntegerField(_("Land"), default=0)
    garage = models.IntegerField(_("Garage"), default=0)
    location = models.CharField(
        _("Location"), choices=CHOICES, max_length=20, default="Inferior"
    )
    construction = models.CharField(
        _("Construction"), choices=CHOICES, max_length=20, default="Inferior"
    )
    accommodation = models.CharField(
        _("Accommodation"), choices=CHOICES, max_length=20, default="Inferior"
    )
    improvements = models.CharField(
        _("Improvements"), choices=CHOICES, max_length=20, default="Inferior"
    )
    sale_date = models.DateField(_("Sale Date"), null=True, blank=True)
    sale_price = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    overall_comparability = models.CharField(
        _("Overall Comparability"),
        choices=CHOICES,
        max_length=20,
        default="Inferior",
    )


class SaleComparableSales(models.Model):
    CHOICES = (
        ("Inferior", "Inferior"),
        ("Comparable", "Comparable"),
        ("Superior", "Superior"),
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="comparable_sales",
        null=True,
        blank=True,
    )
    address = models.CharField(
        _("Address"), max_length=200, null=True, blank=True
    )
    beds = models.IntegerField(_("Beds"), default=0)
    bath = models.IntegerField(_("Bath"), default=0)
    land = models.IntegerField(_("Land"), default=0)
    garage = models.IntegerField(_("Garage"), default=0)
    location = models.CharField(
        _("Location"), choices=CHOICES, max_length=20, default="Inferior"
    )
    construction = models.CharField(
        _("Construction"), choices=CHOICES, max_length=20, default="Inferior"
    )
    accommodation = models.CharField(
        _("Accommodation"), choices=CHOICES, max_length=20, default="Inferior"
    )
    improvements = models.CharField(
        _("Improvements"), choices=CHOICES, max_length=20, default="Inferior"
    )
    sale_date = models.DateField(_("Sale Date"), null=True, blank=True)
    sale_price = models.CharField(
        max_length=50, validators=[number_regex], null=True, blank=True
    )
    overall_comparability = models.CharField(
        _("Overall Comparability"),
        choices=CHOICES,
        max_length=20,
        default="Inferior",
    )


class PurchaseComparableSalesImages(models.Model):
    comparable_sale = models.ForeignKey(
        PurchaseComparableSales,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="comparable_sales/", blank=True)
    image_title = models.CharField(
        _("Image Title"), max_length=100, null=True, blank=True
    )


class SaleComparableSalesImages(models.Model):
    comparable_sale = models.ForeignKey(
        SaleComparableSales,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="comparable_sales/", blank=True)
    image_title = models.CharField(
        _("Image Title"), max_length=100, null=True, blank=True
    )


# This Model is created for those properties whose renovation is required
class Renovation(models.Model):
    purchase = models.OneToOneField(
        Purchase,
        related_name="renovation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    current_expenses = models.CharField(
        _("Current Expenses"),
        validators=[number_regex],
        max_length=50,
        null=True,
        blank=True,
        default=0,
    )
    negative_regex = RegexValidator(
        regex=r"^[\d\,\-]*$", message="Enter Integer numbers."
    )
    renovation_difference = models.CharField(
        _("Difference"),
        max_length=50,
        validators=[negative_regex],
        null=True,
        blank=True,
    )
    # Fields for Insurance
    insurer = models.CharField(
        _("Insurer"), max_length=100, null=True, blank=True
    )
    policy_cost = models.CharField(
        _("Policy Cost"),
        validators=[number_regex],
        max_length=50,
        null=True,
        blank=True,
    )
    policy_cover_amount = models.CharField(
        _("Policy Cover Amount"),
        validators=[number_regex],
        max_length=50,
        null=True,
        blank=True,
    )
    policy_start_date = models.DateField(
        _("Policy's Start Date"), null=True, blank=True
    )
    policy_expiry_date = models.DateField(
        _("Policy's Expiry Date"), null=True, blank=True
    )

    def __str__(self):
        return str(self.purchase.deal)


# This model describes a team of co-workers (objects of Contact Model) recruited for renovation
class Team(models.Model):
    renovation = models.OneToOneField(
        Renovation,
        related_name="team",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    contact = models.ManyToManyField(Contact, related_name="team_contacts")


# Rooms Model is created as soon as the Renovation object is created for a praticular property(lead)
class Rooms(models.Model):
    STATUS_CHOICES = (("Complete", "Complete"), ("Incomplete", "Incomplete"))
    renovation = models.ForeignKey(
        Renovation,
        on_delete=models.CASCADE,
        related_name="rooms",
        null=True,
        blank=True,
    )
    # Fields for all 8 models
    parking = models.OneToOneField(
        Parking,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    entry = models.OneToOneField(
        Entry,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    lounge = models.OneToOneField(
        Lounge,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    dining = models.OneToOneField(
        Dining,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    kitchen = models.OneToOneField(
        Kitchen,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    laundry = models.OneToOneField(
        Laundry,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    bathroom = models.OneToOneField(
        Bathroom,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    bedroom = models.OneToOneField(
        Bedroom,
        related_name="room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # Duration Fields
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    completion_date = models.DateField(
        _("Completion Due"), null=True, blank=True
    )
    duration = models.IntegerField(
        _("Duration"), null=True, blank=True, default=0
    )
    room_thoughts = models.CharField(
        _("Thoughts"), max_length=300, null=True, blank=True
    )
    # Per room expenses
    room_budget = models.CharField(
        _("Room Budget"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    room_total_cost = models.CharField(
        _("Room Total Cost"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    negative_regex = RegexValidator(
        regex=r"^[\d\,\-]*$", message="Enter Integer numbers."
    )
    room_difference = models.CharField(
        _("Savings / Blow Out"),
        max_length=50,
        validators=[negative_regex],
        null=True,
        blank=True,
        default=0,
    )
    status = models.CharField(
        _("Status"),
        choices=STATUS_CHOICES,
        max_length=20,
        default="Incomplete",
    )

    def __str__(self):
        if self.parking:
            if self.parking.location_name:
                return self.parking.location_name
            else:
                return ""
        elif self.entry:
            if self.entry.location_name:
                return self.entry.location_name
            else:
                return ""
        elif self.lounge:
            if self.lounge.location_name:
                return self.lounge.location_name
            else:
                return ""
        elif self.dining:
            if self.dining.location_name:
                return self.dining.location_name
            else:
                return ""
        elif self.kitchen:
            if self.kitchen.location_name:
                return self.kitchen.location_name
            else:
                return ""
        elif self.laundry:
            if self.laundry.location_name:
                return self.laundry.location_name
            else:
                return ""
        elif self.bathroom:
            if self.bathroom.location_name:
                return self.bathroom.location_name
            else:
                return ""
        else:
            if self.bedroom.location_name:
                return self.bedroom.location_name
            else:
                return ""


# Tasks model describes what all tasks are to be performed in a particular room for renovation
class Tasks(models.Model):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    service_man = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    task = models.CharField(_("Task"), max_length=200, null=True, blank=True)
    status = models.BooleanField(_("Completed"), default=False)
    quote_number = models.IntegerField(_("Quote #"), null=True, blank=True)
    invoice_number = models.IntegerField(_("Invoice #"), null=True, blank=True)
    total = models.CharField(
        _("Total"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )


class InternalTasksForMyself(models.Model):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name="tasks_for_myself",
        null=True,
        blank=True,
    )
    task_name = models.CharField(
        _("Task"), max_length=200, null=True, blank=True
    )
    completion_status = models.BooleanField(_("Completed"), default=False)


# Photo model will be used to store photos corresponding to a renovation
class Images(models.Model):
    CATEGORY_CHOICES = (
        ("Before-Renovation", "Before-Renovation"),
        ("After-Renovation", "After-Renovation"),
    )
    renovation = models.ForeignKey(
        Renovation,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.FileField(upload_to="renovation/", null=False, blank=False)
    image_title = models.CharField(
        _("Image Title"), max_length=100, null=True, blank=True
    )
    category = models.CharField(
        _("Category"),
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Before-Renovation",
    )


class Materials(models.Model):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name="materials",
        null=True,
        blank=True,
    )
    description = models.CharField(
        _("Description"), max_length=100, null=True, blank=True
    )
    quantity = models.IntegerField(_("Quantity"), null=True, blank=True)
    price = models.CharField(
        _("Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    total = models.CharField(
        _("Total"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )


class PrimeCostItems(models.Model):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name="prime_cost_items",
        null=True,
        blank=True,
    )
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    description = models.CharField(
        _("Description"), max_length=100, null=True, blank=True
    )
    item_number = models.IntegerField(_("Item #"), null=True, blank=True)
    quantity = models.IntegerField(_("Quantity"), null=True, blank=True)
    price = models.CharField(
        _("Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    total = models.CharField(
        _("Total"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )


# Model for storing my details for a purchase of a property
class MyPurchaseDetails(models.Model):
    MONEY_LENDER_CHOICES = (
        ("Bank", "Bank"),
        ("Private Lender", "Private Lender"),
    )
    purchase = models.OneToOneField(
        Purchase,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_purchase_details",
    )
    entity = models.ForeignKey(
        "settings.entity",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_entity_details",
    )
    accountant = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_accountant_details",
    )
    agent = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_agent_details",
    )
    conveyancer = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_conveyancer_details",
    )
    bank = models.OneToOneField(
        Bank,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_bank_details",
    )
    money_lender = models.CharField(
        _("Money Lender"),
        choices=MONEY_LENDER_CHOICES,
        max_length=50,
        default="Bank",
    )


class PurchaseCorrespondanceDocuments(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="purchase_correspondance_documents",
    )
    document = models.FileField(
        _("Document"),
        upload_to="purchase/correspondance",
        null=True,
        blank=True,
    )
    note = models.CharField(_("Note"), max_length=100, null=True, blank=True)


class External(models.Model):
    STATUS_CHOICES = (("Complete", "Complete"), ("Incomplete", "Incomplete"))
    renovation = models.ForeignKey(
        Renovation,
        on_delete=models.CASCADE,
        related_name="external",
        null=True,
        blank=True,
    )
    location = models.CharField(
        _("Location"), max_length=300, null=False, blank=False
    )
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    completion_date = models.DateField(
        _("Completion Due"), null=True, blank=True
    )
    duration = models.IntegerField(
        _("Duration"), null=True, blank=True, default=0
    )
    thoughts = models.CharField(
        _("Thoughts"), max_length=300, null=True, blank=True
    )
    # Per room expenses
    budget = models.CharField(
        _("Budget"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    total_cost = models.CharField(
        _("Total Cost"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    negative_regex = RegexValidator(
        regex=r"^[\d\,\-]*$", message="Enter Integer numbers."
    )
    difference = models.CharField(
        _("Savings / Blow Out"),
        max_length=50,
        validators=[negative_regex],
        null=True,
        blank=True,
        default=0,
    )
    status = models.CharField(
        _("Status"),
        choices=STATUS_CHOICES,
        max_length=20,
        default="Incomplete",
    )

    def __str__(self):
        if self.location:
            return self.location
        else:
            return ""


class ExternalTasks(models.Model):
    location = models.ForeignKey(
        External,
        on_delete=models.CASCADE,
        related_name="external_tasks",
        null=True,
        blank=True,
    )
    service_man = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="external_tasks",
        null=True,
        blank=True,
    )
    task = models.CharField(_("Task"), max_length=200, null=True, blank=True)
    status = models.BooleanField(_("Completed"), default=False)
    quote_number = models.IntegerField(_("Quote #"), null=True, blank=True)
    invoice_number = models.IntegerField(_("Invoice #"), null=True, blank=True)
    total = models.CharField(
        _("Total"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )


class ExternalMaterials(models.Model):
    location = models.ForeignKey(
        External,
        on_delete=models.CASCADE,
        related_name="external_materials",
        null=True,
        blank=True,
    )
    description = models.CharField(
        _("Description"), max_length=100, null=True, blank=True
    )
    quantity = models.IntegerField(_("Quantity"), null=True, blank=True)
    price = models.CharField(
        _("Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )
    total = models.CharField(
        _("Total"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
        default=0,
    )


class ExternalTasksForMyself(models.Model):
    location = models.ForeignKey(
        External,
        on_delete=models.CASCADE,
        related_name="external_tasks_for_myself",
        null=True,
        blank=True,
    )
    task_name = models.CharField(
        _("Task"), max_length=200, null=True, blank=True
    )
    completion_status = models.BooleanField(_("Completed"), default=False)


class AFCAComplaintLodged(models.Model):
    STATUS_CHOICES = (("Yes", "Yes"), ("No", "No"))
    deal = models.OneToOneField(
        Deal,
        on_delete=models.CASCADE,
        related_name="afca_complaint_lodged",
        null=True,
        blank=True,
    )
    complaint_lodged_status = models.CharField(
        _("Complaint Lodged"),
        choices=STATUS_CHOICES,
        max_length=10,
        default="No",
    )
    contact_name = models.CharField(
        _("Contact Name"), max_length=100, null=True, blank=True
    )
    date = models.DateField(_("Date"), null=True, blank=True)
    afca_case_number = models.CharField(
        _("AFCA Case Number"), max_length=100, null=True, blank=True
    )
    mobile_regex = RegexValidator(
        regex=r"^[(\d) ]{10,15}$",
        message="Mobile number must be entered in the format: 'XXXXXXXXXX' or '(XX) XXXXXXXXXX'. Up to 12 digits allowed.",
    )
    mobile = models.CharField(
        validators=[mobile_regex], max_length=17, null=True, blank=True
    )  # validators should be a list
    email = models.EmailField(_("Email"), null=True, blank=True)
    comments = models.CharField(
        _("Comments"), max_length=100, null=True, blank=True
    )


class ListForSale(models.Model):
    SALE_METHOD_CHOICES = (
        ("Auction", "Auction"),
        ("Private Treaty", "Private Treaty"),
        ("Tender", "Tender"),
    )
    RESULT_CHOICES = (("Sold", "Sold"), ("Passed In", "Passed In"))
    deal = models.OneToOneField(
        Deal,
        on_delete=models.CASCADE,
        related_name="list_for_sale",
        null=True,
        blank=True,
    )
    real_estate_company_agent = models.OneToOneField(
        Contact, on_delete=models.CASCADE, related_name="real_estate_agent"
    )
    percentage_regex = RegexValidator(
        regex=r"^[\d\,.]*$", message="Enter whole numbers."
    )
    commission_percentage = models.CharField(
        _("Listed Price"),
        max_length=50,
        validators=[percentage_regex],
        null=True,
        blank=True,
    )
    agreement_date = models.DateField(
        _("Agreement Date"), null=True, blank=True
    )
    agreement_market_value = models.CharField(
        _("Agreement Market Value"),
        max_length=50,
        validators=[number_regex],
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
    price_drop = models.CharField(
        _("Price Drop"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    sale_method = models.CharField(
        _("Sale Method"),
        choices=SALE_METHOD_CHOICES,
        max_length=50,
        default="Auction",
    )
    auction_date = models.DateField(_("Auction Date"), null=True, blank=True)
    advertising_costs = models.CharField(
        _("Advertising Costs"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    result = models.CharField(
        _("Result"), choices=RESULT_CHOICES, max_length=50, default="Sold"
    )


class Sold(models.Model):
    deal = models.OneToOneField(
        Deal,
        on_delete=models.CASCADE,
        related_name="sold",
        null=True,
        blank=True,
    )
    date_sold = models.DateField(_("Date Sold"), default=datetime.date.today)
    exchange_date = models.DateField(_("Exchange Date"), null=True, blank=True)
    completion_time = models.IntegerField(
        _("Completion Time"), null=True, blank=True
    )
    completion_date = models.DateField(
        _("Completion Date"), null=True, blank=True
    )
    settlement_date = models.DateField(
        _("Settlement Date"), null=True, blank=True
    )
    listed_price = models.CharField(
        _("Listed Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    sale_price = models.CharField(
        _("Sale Price"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    difference = models.CharField(
        _("Difference"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


class Solicitor(models.Model):
    lawFirm = models.CharField(max_length=100)
    contactName = models.CharField(max_length=300)
    postalAddress = models.CharField(max_length=400)
    mobile = models.CharField(max_length=10)
    officePhone = models.PositiveIntegerField(default=0)
    officeFax = models.PositiveIntegerField(default=0)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)
    # deal = models.ForeignKey(
    #     Deal, on_delete=models.CASCADE, null=True, blank=True)

    def get_id(self, obj):
        return obj.id

    def __str__(self):
        return self.lawFirm

    def get_absolute_url(self):
        return reverse('dashboard:deals:owner_details')

    def clean(self):
        model = self.__class__
        if len(str(self.mobile)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")


class Agent(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:deals:agentlist')

    def clean(self):
        model = self.__class__
        if len(str(self.phone)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")


class BankNew(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:deals:banklist')

    def clean(self):
        model = self.__class__
        if len(str(self.phone)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")


class Executor(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:deals:executorlist')

    def clean(self):
        model = self.__class__
        if len(str(self.phone)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")


class Liquidator(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:deals:liquidatorlist')

    def clean(self):
        model = self.__class__
        if len(str(self.phone)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")


class Family(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:deals:familylist')

    def clean(self):
        model = self.__class__
        if len(str(self.phone)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")


class Other(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_by=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:deals:otherlist')

    def clean(self):
        model = self.__class__
        if len(str(self.phone)) != 10:
            raise ValidationError("Phone number must be 10 digits long!! ")
