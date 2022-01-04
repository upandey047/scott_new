from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from deals.models import Deal, MyPurchaseDetails
from django.core.validators import RegexValidator
from deals.models import (
    Purchase,
    PurchaseCosts,
    HoldingCosts,
    Sale,
    FeasibilityReport,
)


class Address(models.Model):
    individual = models.ForeignKey(
        "Individual", on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, null=True, blank=True
    )
    trust = models.ForeignKey(
        "Trust", on_delete=models.CASCADE, null=True, blank=True
    )
    po_box = models.CharField(
        _("PO Box"), max_length=100, null=True, blank=True
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

    def __str__(self):
        return str(self.unit) + " " + str(self.post_code)


# RegisteredAddressForm will be used for company entity only
class RegisteredAddress(models.Model):
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, null=True, blank=True
    )
    po_box = models.CharField(
        _("PO Box"), max_length=100, null=True, blank=True
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

    def __str__(self):
        return str(self.unit) + " " + str(self.post_code)


class Email(models.Model):
    email = models.EmailField(
        _("Email"), max_length=100, unique=True, blank=True
    )
    individual = models.ForeignKey(
        "Individual", on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, null=True, blank=True
    )
    trust = models.ForeignKey(
        "Trust", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.email


class Documents(models.Model):
    logo = models.FileField(upload_to="documents/", null=True, blank=True)
    signature = models.FileField(upload_to="documents/", null=True, blank=True)


class Individual(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    mobile_regex = RegexValidator(
        regex=r"^[(\d) ]{10,15}$",
        message="Mobile number must be entered in the format: 'XXXXXXXXXX' or '(XX) XXXXXXXXXX'. Up to 12 digits allowed.",
    )
    mobile = models.CharField(
        validators=[mobile_regex], max_length=17, null=True, blank=True
    )  # validators should be a list
    documents = models.OneToOneField(
        Documents, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    ABN_ACN_CHOICES = (
        ("ABN", "ABN"),
        ("ACN", "ACN"),
        ("Not Present", "Not Present"),
    )
    GST_REGISTERED_CHOICES = (("YES", "YES"), ("NO", "NO"))
    company = models.CharField(_("Company"), max_length=100)
    abn_or_acn = models.CharField(
        _("ABN/ACN"), max_length=15, choices=ABN_ACN_CHOICES, default="ABN"
    )
    abn_or_acn_number = models.IntegerField(
        _("ABN/ACN Number"), null=True, blank=True
    )
    mobile_regex = RegexValidator(
        regex=r"^[(\d) ]{10,15}$",
        message="Mobile number must be entered in the format: 'XXXXXXXXXX' or '(XX) XXXXXXXXXX'. Up to 12 digits allowed.",
    )
    mobile = models.CharField(
        validators=[mobile_regex], max_length=17, null=True, blank=True
    )  # validators should be a list
    gst_registered = models.CharField(
        _("GST Registered"),
        max_length=5,
        choices=GST_REGISTERED_CHOICES,
        default="NO",
    )
    documents = models.OneToOneField(
        Documents, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.company


class Shares(models.Model):
    trust = models.ForeignKey(
        "Trust", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    number_regex = RegexValidator(
        regex=r"^[\d\,]*$", message="Enter whole numbers."
    )
    amount = models.CharField(
        default=0,
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


class Trust(models.Model):
    TRUST_TYPE_CHOICES = (
        ("Unit", "Unit"),
        ("Discretionary", "Discretionary"),
        ("Hybrid", "Hybrid"),
        ("SMSF", "SMSF"),
    )
    company = models.CharField(_("Company"), max_length=100)
    trust_name = models.CharField(_("Trust Name"), max_length=100)
    trust_type = models.CharField(
        _("Trust Type"),
        max_length=20,
        choices=TRUST_TYPE_CHOICES,
        default="Unit",
    )
    bare_trust_details = models.CharField(
        _("Bare Trust Details"), max_length=100, null=True, blank=True
    )
    documents = models.OneToOneField(
        Documents, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.trust_name


class Entity(models.Model):
    ENTITY_TYPE_CHOICES = (
        ("individual", "individual"),
        ("company", "company"),
        ("trust", "trust"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    entity_type = models.CharField(
        _("Entity Type"), max_length=30, choices=ENTITY_TYPE_CHOICES
    )
    individual = models.OneToOneField(
        Individual, on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    trust = models.OneToOneField(
        Trust, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        if self.individual:
            return str(self.individual)
        elif self.company:
            return str(self.company)
        else:
            return str(self.trust)

    def entity(self):
        if self.individual:
            return self.individual
        elif self.company:
            return self.company
        else:
            return self.trust


# Models for checklist
class Category(models.Model):
    category_name = models.CharField(_("Category"), max_length=100)

    def __str__(self):
        return self.category_name


class Event(models.Model):
    event_name = models.CharField(_("Event"), max_length=100)
    default_event = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name


class CheckList(models.Model):
    COMPLETE_CHOICES = (("Yes", "Yes"), ("No", "No"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(_("Date"), default=datetime.date.today)
    complete = models.CharField(
        _("Complete"), max_length=5, choices=COMPLETE_CHOICES, default="No"
    )

    def __str__(self):
        return str(self.category) + " " + str(self.event)


class DefaultCheckList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(self.category) + " " + str(self.event)


"""
Signal to create default values of checklist whenever a user gets created
There will be certain events which will be default events. Whenever a user is created, checklist objects will be created for the user with the default events
Whenever a user will create a new event, it will be added to the Events table with default_event flag as False. For a new event, if the event already exists
in the Event table, then that object will be associated to the newly created checklist. Else, a new event object will be created and associated to the newly
created checklist object.
"""


@receiver(post_save, sender=User)
def my_handler(sender, **kwargs):
    if kwargs["created"] is True:
        user_instance = kwargs["instance"]
        initial_research = Category.objects.get(
        category_name="initial_research"
        )
        # except Category.DoesNotExist:
        #     pass
            
        
        letters = Category.objects.get(category_name="letters")
        inspection = Category.objects.get(category_name="inspection")
        due_diligence = Category.objects.get(category_name="due_diligence")
        property_searches = Category.objects.get(
            category_name="property_searches"
        )
        offer_or_finance = Category.objects.get(
            category_name="offer_or_finance"
        )
        renovation = Category.objects.get(category_name="renovation")
        market_research = Category.objects.get(category_name="market_research")
        exchange_or_settlement = Category.objects.get(
            category_name="exchange_or_settlement"
        )
        listing_for_sale = Category.objects.get(
            category_name="listing_for_sale"
        )
        sale_exchange_or_settlement = Category.objects.get(
            category_name="sale-exchange_or_settlement"
        )

        DefaultCheckList.objects.create(
            user=user_instance,
            category=initial_research,
            event=Event.objects.get(event_name="RP Data Search of Property"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=initial_research,
            event=Event.objects.get(event_name="On The House.com.au"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=initial_research,
            event=Event.objects.get(event_name="Block Brief"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=initial_research,
            event=Event.objects.get(
                event_name="Real Estate.com.au - Stock on market"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=initial_research,
            event=Event.objects.get(
                event_name="Real Estate.com.au - Stock Sold"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=initial_research,
            event=Event.objects.get(event_name="DSR Score"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 1 - Owner"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 2 - Owner"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 3 - Owner"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 1 - Bank"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 2 - Bank"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 3 - Bank"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 1 - Lawyer"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 2 - Lawyer"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=letters,
            event=Event.objects.get(event_name="Send Letter 3 - Lawyer"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=inspection,
            event=Event.objects.get(event_name="Inspection Organised"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=inspection,
            event=Event.objects.get(event_name="Inspection Carried Out"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=inspection,
            event=Event.objects.get(event_name="Inspection Sheet"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=inspection,
            event=Event.objects.get(event_name="Interview Owner"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=inspection,
            event=Event.objects.get(event_name="Photos"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(
                event_name="Assess property at first glance"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(event_name="Assess Neighbourhood"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(
                event_name="Research Subject Property Information"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(
                event_name="Professional Building Inspection"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(event_name="Professional Pest Inspection"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(event_name="Survey Report"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=due_diligence,
            event=Event.objects.get(event_name="Engineering Report"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Title Search"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Strata Search"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Encumbrance Search"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Building Record Search"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Flood Zone Search"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Bushfire Search"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Survey Report"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=property_searches,
            event=Event.objects.get(event_name="Contract For Sale"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Offer Created"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Offer Submitted"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Offer Accepted"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Offer Declined"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Terms of Agreement"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Engage Broker / Bank"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Pre Approval"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Formal Approval"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Engage Legal Team"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=offer_or_finance,
            event=Event.objects.get(event_name="Prepare Contact - Legal Team"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(
                event_name="Engage Local Council for project requirements"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(
                event_name="Engage Builder / Trades People"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(
                event_name="Engage Architect / Drafts Person"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(event_name="Engage Engineer"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(event_name="Pay DA Fees"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(event_name="Lodge DA"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(event_name="Confirm Materials & PC Items"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=renovation,
            event=Event.objects.get(event_name="Determine Renovation Budget"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Stock On Market"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Avg Days on Market"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Demographics"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Comparable Sales"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(
                event_name="Deposit Paid - .25% - Cool Off Period"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Deposit Paid - 10%"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Exchange"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Confirm Net Funds Available"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Settlement"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Collect Keys"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Arrange Market Appraisal"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Engage Valuer"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Engage Agent"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Determine Minimum Sale Price"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="List Property For Sale"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(
                event_name="Engage Legal Firm - Contract For Sale"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=market_research,
            event=Event.objects.get(event_name="Prepare Property For Sale"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=exchange_or_settlement,
            event=Event.objects.get(
                event_name="Deposit Paid - .25% - Cool Off Period"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=exchange_or_settlement,
            event=Event.objects.get(event_name="Deposit Paid - 10%"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=exchange_or_settlement,
            event=Event.objects.get(event_name="Exchange"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=exchange_or_settlement,
            event=Event.objects.get(event_name="Confirm Net Funds Available"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=exchange_or_settlement,
            event=Event.objects.get(event_name="Settlement"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=exchange_or_settlement,
            event=Event.objects.get(event_name="Collect Keys"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(event_name="Arrange Market Appraisal"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(event_name="Engage Valuer"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(event_name="Engage Agent"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(event_name="Determine Minimum Sale Price"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(event_name="List Property For Sale"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(
                event_name="Engage Legal Firm - Contract For Sale"
            ),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=listing_for_sale,
            event=Event.objects.get(event_name="Prepare Property For Sale"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=sale_exchange_or_settlement,
            event=Event.objects.get(event_name="Negotiate Terms of Contract"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=sale_exchange_or_settlement,
            event=Event.objects.get(event_name="Purchaser To Pay Deposit"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=sale_exchange_or_settlement,
            event=Event.objects.get(event_name="Exchange"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=sale_exchange_or_settlement,
            event=Event.objects.get(event_name="Confirm Net Funds Available"),
        )
        DefaultCheckList.objects.create(
            user=user_instance,
            category=sale_exchange_or_settlement,
            event=Event.objects.get(event_name="Settlement"),
        )


"""
Signal to create Checklist objects and offer details objects
Whenever a new deal object is created, checklist objects should be created for the user. All Default checklist objects are fetched from the database and
checklist objects for the given deal are created.
Also, offer details objects should be created for the time the deal goes through
"""


@receiver(post_save, sender=Deal)
def signal_on_deal_creation(sender, **kwargs):
    if kwargs["created"] is True:
        deal_obj = kwargs["instance"]
        user = deal_obj.lead.user
        default_checklists = DefaultCheckList.objects.filter(user=user)
        for checklist in default_checklists:
            CheckList.objects.create(
                user=user,
                deal=kwargs["instance"],
                category=checklist.category,
                event=checklist.event,
            )

        purchase_obj = Purchase.objects.create(deal=deal_obj)
        Sale.objects.create(deal=deal_obj)
        PurchaseCosts.objects.create(
            purchase=purchase_obj, name="Inspection - Building", amount=0
        )
        PurchaseCosts.objects.create(
            purchase=purchase_obj, name="Inspection - Pest", amount=0
        )
        PurchaseCosts.objects.create(
            purchase=purchase_obj, name="Legal Fees", amount=0
        )
        PurchaseCosts.objects.create(
            purchase=purchase_obj, name="Loan Fees", amount=0
        )
        PurchaseCosts.objects.create(
            purchase=purchase_obj, name="Stamp Duty", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Council Rates(6 months)", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Council Rates - Arrears", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Council Water(6 months)", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Council Water - Arrears", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Insurance", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Land Tax", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Land Tax - Arrears", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Strata Fees (6 Months)", amount=0
        )
        HoldingCosts.objects.create(
            purchase=purchase_obj, name="Strata Fees Arrears", amount=0
        )
        FeasibilityReport.objects.create(purchase=purchase_obj)

        # Create MyPurchaseDetails object after the creation of purchase
        MyPurchaseDetails.objects.create(purchase=purchase_obj)
