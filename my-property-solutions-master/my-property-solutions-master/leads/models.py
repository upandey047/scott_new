from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class Lead(models.Model):
    """
    Created when a new lead is created by user.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("active", "Active"),
        ("purchased", "Purchased"),
        ("listed", "Listed"),
        ("sold", "Sold"),
        ("not_proceeding", "Not Proceeding"),
    )
    CATEGORY_CHOICES = (
        # ("bankruptcy", "Bankruptcy"),
        # ("deceased", "Deceased Estate"),
        # ("divorce", "Divorce"),
        # ("liquidation", "Liquidation"),
        # ("mortgagee", "Mortgagee"),
        # ("sheriff", "Sheriff"),
        ("off-market", "Off Market"),
        ("on-market", "On Market"),
        ("other", "Other"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(_("Category"), choices=CATEGORY_CHOICES, max_length=20)
    note = models.CharField(max_length=255, verbose_name="Note if other", blank=True)
    status = models.CharField(_("Status"), choices=STATUS_CHOICES, max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    


class Property(models.Model):
    """
    Details of a property, created when a lead is created
    """

    ON_OFF_CHOICES = (("ON", "ON"), ("OFF", "OFF"))
    PROPERTY_TYPE_CHOICES = (
        ("Residential", "Residential"),
        ("Strata", "Strata"),
    )
    lead = models.OneToOneField(Lead,on_delete=models.CASCADE,related_name="property",null=True,blank=True,)
    property_type = models.CharField(_("Property Type"),max_length=30,choices=PROPERTY_TYPE_CHOICES,default="Residential",)
    beds = models.IntegerField(_("Beds"), default=0)
    bath = models.IntegerField(_("Bath"), default=0)
    land = models.IntegerField(_("Land"), default=0)
    garage = models.IntegerField(_("Garage"), default=0)
    po_box = models.CharField(_("PO Box"), max_length=100, null=True, blank=True)
    postal_suburb = models.CharField(_("Suburb"), max_length=100, null=True, blank=True)
    postal_state = models.CharField(_("State"), max_length=100, null=True, blank=True)
    postal_post_code = models.CharField(_("Post Code"), max_length=100, null=True, blank=True)
    unit = models.CharField(_("Unit"), max_length=100, null=True, blank=True)
    number = models.IntegerField(_("Number"), null=True, blank=True)
    street = models.CharField(_("Street"), max_length=100, null=True, blank=True)
    suburb = models.CharField( _("Suburb"), max_length=100, null=True, blank=True)
    state = models.CharField(_("State"), max_length=100, null=True, blank=True)
    post_code = models.CharField(_("Post Code"), max_length=100, null=True, blank=True)
    original_list_date = models.DateField(_("Original List Date"), null=True, blank=True)
    todays_date = models.DateField(_("Today's Date"), null=True, blank=True)
    on_or_off_market = models.CharField(_("On Or Off Market"),max_length=3,choices=ON_OFF_CHOICES,default="ON",)
    number_regex = RegexValidator(regex=r"^[\d\,-]*$", message="Enter whole numbers.")
    start_list_price = models.CharField(_("Start List Price"), max_length=50,validators=[number_regex],null=True,blank=True,)
    end_list_price = models.CharField(_("End List Price"),max_length=50,validators=[number_regex],null=True,blank=True,
    )
    start_list_date = models.DateField(
        _("Start List Date"), null=True, blank=True
    )
    end_list_date = models.DateField(_("End List Date"), null=True, blank=True)
    difference = models.CharField(
        _("Difference"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    dom = models.IntegerField(_("Days On Market"), null=True, blank=True)

    def address(self):
        address_parts = []
        if self.unit:
            address_parts.append("Unit " + self.unit + ",")
        if self.number:
            address_parts.append(str(self.number))
        if self.street:
            address_parts.append(self.street)
        if self.suburb:
            address_parts.append(self.suburb)
        if self.state:
            address_parts.append(self.state)
        if self.post_code:
            address_parts.append(self.post_code)
        return " ".join(address_parts)


class Auction(models.Model):
    """
    This will only be there for Sheriff
    """

    _property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name="property_auction",null=True,blank=True,)
    date = models.DateField(_("Date"), null=True, blank=True)
    time = models.TimeField(_("Time"), null=True, blank=True)
    location = models.CharField(_("Location"), max_length=50, null=True, blank=True)
    number_regex = RegexValidator(regex=r"^[\d\,]*$", message="Enter whole numbers.")
    deposit_required = models.CharField(_("Deposit Required"),max_length=50,validators=[number_regex],null=True,blank=True,)
    days = models.IntegerField(_("Days (Balance Due After)"), null=True, blank=True)


class PropertyOwner(models.Model):
    """
    Owner of a property, creeated when a new property is created after cretion of lead
    """

    ABN_ACN_CHOICES = (
        ("ABN", "ABN"),
        ("ACN", "ACN"),
        ("Not Present", "Not Present"),
    )
    _property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="property_owner",
        null=True,
        blank=True,
    )
    first_name = models.CharField(_("First Name"), max_length=100,blank=True,null=True)
    last_name = models.CharField(_("Last Name"), max_length=100,blank=True,null=True)
    title = models.CharField(_("Title"), max_length=100, null=True, blank=True)
    salutation = models.CharField(
        _("Salutation"), max_length=100, null=True, blank=True
    )
    mobile_regex = RegexValidator(
        regex=r"^[(\d) ]{10,15}$",
        message="Mobile number must be entered in the format: 'XXXXXXXXXX' or '(XX) XXXXXXXXXX'. Up to 12 digits allowed.",
    )
    mobile = models.CharField(
        validators=[mobile_regex], max_length=17, null=True, blank=True
    )  # validators should be a list
    email = models.EmailField(
        _("Email"), max_length=100, null=True, blank=True
    )
    date_of_notice = models.DateField(
        _("Date Of Notice"), null=True, blank=True
    )
    date_of_death = models.DateField(_("Date Of Death"), null=True, blank=True)
    deceased = models.CharField(
        _("Deceased"), max_length=100, null=True, blank=True
    )
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(
        _("Company Name"), max_length=100, null=True, blank=True
    )
    abn_or_acn = models.CharField(
        _("ABN/ACN"), max_length=15, choices=ABN_ACN_CHOICES, default="ABN"
    )
    abn_or_acn_number = models.IntegerField(
        _("ABN/ACN Number"), null=True, blank=True
    )
    # postal details' fields
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

    def __str__(self):
        return self.first_name + " " + self.last_name


class Bank(models.Model):
    """
    the bank a/c For an owner of a property this will store the bank details
    """

    STATUS_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="bank",
        null=True,
        blank=True,
    )
    mortgaged = models.CharField(
        _("Mortgaged"), choices=STATUS_CHOICES, max_length=50, default="No"
    )
    bank = models.CharField(_("Bank"), max_length=100, null=True, blank=True)
    reference = models.CharField(
        _("Reference"), max_length=100, null=True, blank=True
    )
    legal_representative = models.CharField(
        _("Legal Representative"), max_length=100, null=True, blank=True
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
        max_length=17,
        null=True,
        blank=True,
    )
    email = models.EmailField(_("Email"), null=True, blank=True)
    mortgage_number = models.CharField(
        _("Mortgage Number"), max_length=100, null=True, blank=True
    )
    number_regex = RegexValidator(
        regex=r"^[\d\,.]*$", message="Enter whole numbers."
    )
    original_amount = models.CharField(
        _("Original Loan Amount"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    current_amount = models.CharField(
        _("Current Loan Amount"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    arrears = models.CharField(
        _("Arrears Amount"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )
    interest = models.DecimalField(
        _("Interest"), max_digits=5, decimal_places=2, null=True, blank=True
    )
    duration_in_years = models.IntegerField(
        _("Duration (Years)"), null=True, blank=True
    )
    repayments = models.CharField(
        _("Repayments"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.bank)


class PersonalLoan(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    number_regex = RegexValidator(
        regex=r"^[\d\,]*$", message="Enter whole numbers."
    )
    amount = models.CharField(
        _("Amount"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


class Title(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, null=True, blank=True
    )
    name_of_caveat = models.CharField(
        _("Name Of Caveat"), max_length=100, null=True, blank=True
    )
    number_regex = RegexValidator(
        regex=r"^[\d\,]*$", message="Enter whole numbers."
    )
    value_of_caveat = models.CharField(
        _("Value"),
        max_length=50,
        validators=[number_regex],
        null=True,
        blank=True,
    )


class Dealing(models.Model):
    DEALING_TYPE_CHOICES = (
        ("Caveat", "Caveat"),
        ("Covenant", "Covenant"),
        ("Easement", "Easement"),
        ("Mortgage", "Mortgage"),
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, null=True, blank=True
    )
    dealing_type = models.CharField(
        _("Dealing Type"),
        choices=DEALING_TYPE_CHOICES,
        max_length=50,
        blank=True,
    )


# Inspection Sheet models
class LandDetails(models.Model):
    """
    Land details of a property
    """

    TYPE_CHOICES = (
        ("Acreage", "Acreage"),
        ("Apartment", "Apartment"),
        ("House", "House"),
        ("Rural", "Rural"),
        ("Townhouse", "Townhouse"),
        ("Vacant Land", "Vacant Land"),
        ("Villa", "Villa"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="land_details",
        null=True,
        blank=True,
    )
    type = models.CharField(
        _("Property Type"),
        max_length=20,
        choices=TYPE_CHOICES,
        default="Acreage",
    )
    lot = models.CharField(_("Lot"), max_length=100, null=True, blank=True)
    dp_or_sp = models.CharField(_("DP/SP Number"), max_length=10)
    section = models.CharField(
        _("Section"), max_length=100, null=True, blank=True
    )


class Zoning(models.Model):
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="zoning",
        null=True,
        blank=True,
    )
    zoning = models.CharField(
        _("Zoning"), max_length=100, null=True, blank=True
    )


class Shape(models.Model):
    SHAPE_CHOICES = (
        ("Regular", "Regular"),
        ("Irregular", "Irregular"),
        ("Corner", "Corner"),
    )
    CONTOUR_CHOICES = (
        ("Cross Fall", "Cross Fall"),
        ("Rise", "Rise"),
        ("Fall", "Fall"),
        ("Level", "Level"),
    )
    DEGREE_CHOICES = (
        ("Gentle", "Gentle"),
        ("Moderate", "Moderate"),
        ("Steep", "Steep"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="shape",
        null=True,
        blank=True,
    )
    shape = models.CharField(
        _("Shape"), choices=SHAPE_CHOICES, max_length=100, default="Regular"
    )
    contour = models.CharField(
        _("Contour"),
        choices=CONTOUR_CHOICES,
        max_length=100,
        default="Cross Fall",
    )
    degree = models.CharField(
        _("Degree"), choices=DEGREE_CHOICES, max_length=100, default="Gentle"
    )


class StreetAppeal(models.Model):
    DESCRIPTION_CHOICES = (
        ("Poor", "Poor"),
        ("Average", "Average"),
        ("Above Average", "Above Average"),
        ("Excellent", "Excellent"),
    )
    LANDSCAPING_CHOICES = (
        ("Poor", "Poor"),
        ("Average", "Average"),
        ("Above Average", "Above Average"),
        ("Excellent", "Excellent"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="street_appeal",
        null=True,
        blank=True,
    )
    description = models.CharField(
        _("Description"),
        choices=DESCRIPTION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    landscaping = models.CharField(
        _("Landscaping"),
        choices=LANDSCAPING_CHOICES,
        max_length=100,
        default="Excellent",
    )
    street_appeal_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )


class Construction(models.Model):
    LEVELS_CHOICES = (("1", "1"), ("2", "2"), ("3", "3"))
    FOUNDATION_CHOICES = (
        ("Piers", "Piers"),
        ("Pole", "Pole"),
        ("Slab", "Slab"),
    )
    EXTERNAL_WALLS_CHOICES = (
        ("Blue board", "Blue board"),
        ("Brick", "Brick"),
        ("Cladding - Metal", "Cladding - Metal"),
        ("Cladding - Stone", "Cladding - Stone"),
        ("Cladding - Vinyl", "Cladding - Vinyl"),
        ("Cladding - Wood", "Cladding - Wood"),
        ("Colourbond", "Colourbond"),
        ("Concrete", "Concrete"),
        ("Concrete Blocks", "Concrete Blocks"),
        ("Fibre Cement", "Fibre Cement"),
        ("Hardiplank", "Hardiplank"),
        ("Render", "Render"),
        ("Rendered - Bagged", "Rendered - Bagged"),
        ("Stone", "Stone"),
    )
    ROOF_DESCRIPTION_CHOICES = (
        ("Colourbond", "Colourbond"),
        ("Cliplock", "Cliplock"),
        ("Concrete Tile", "Concrete Tile"),
        ("Decromastic", "Decromastic"),
        ("Other", "Other"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="construction",
        null=True,
        blank=True,
    )
    levels = models.CharField(
        _("Levels"), choices=LEVELS_CHOICES, max_length=100, default="1"
    )
    building_area = models.IntegerField(
        _("Building Area"), null=True, blank=True
    )
    foundation_description = models.CharField(
        _("Foundation"),
        choices=FOUNDATION_CHOICES,
        max_length=100,
        default="Piers",
    )
    foundation_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    foundation_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    external_walls = models.CharField(
        _("External Walls"),
        choices=EXTERNAL_WALLS_CHOICES,
        max_length=100,
        default="Blue board",
    )
    external_walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    external_walls_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    roof_description = models.CharField(
        _("Roof Description"),
        choices=ROOF_DESCRIPTION_CHOICES,
        max_length=100,
        default="Blue board",
    )
    roof_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    roof_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )


class Parking(models.Model):
    # Carport and Garage choices are same. hence defining carport choices variable only
    CARPORT_CHOICES = (
        ("None", "None"),
        ("Single", "Single"),
        ("Double", "Double"),
        ("Tandem", "Tandem"),
    )
    OTHER_CHOICES = (
        ("None", "None"),
        ("Off Street", "Off Street"),
        ("On Street", "On Street"),
        ("Underground", "Underground"),
        ("Other", "Other"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="parking",
        null=True,
        blank=True,
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    carport = models.CharField(
        _("Carport"), choices=CARPORT_CHOICES, max_length=100, default="Single"
    )
    carport_area = models.IntegerField(
        _("Carport Area"), null=True, blank=True
    )
    garage = models.CharField(
        _("Garage"), choices=CARPORT_CHOICES, max_length=100, default="Single"
    )
    garage_area = models.IntegerField(_("Garage Area"), null=True, blank=True)
    other = models.CharField(
        _("Other"), choices=OTHER_CHOICES, max_length=100, default="Off Street"
    )
    parking_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )


class Features(models.Model):
    POOL_MATERIAL_CHOICES = (
        ("Concrete", "Concrete"),
        ("Fibreglass", "Fibreglass"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    REGISTERED_CHOICES = (("YES", "YES"), ("NO", "NO"))
    FENCING_MATERIAL_CHOICES = (
        ("Brick", "Brick"),
        ("Colourbond", "Colourbond"),
        ("Timber", "Timber"),
        ("Post & Wire", "Post & Wire"),
        ("None", "None"),
        ("Other", "Other"),
    )
    DECK_MATERIAL_CHOICES = (
        ("Concrete", "Concrete"),
        ("Timber", "Timber"),
        ("Tiled", "Tiled"),
        ("Other", "Other"),
    )
    RETAINING_WALLS_CHOICES = (
        ("None", "None"),
        ("Blocks", "Blocks"),
        ("Concrete", "Concrete"),
        ("Sleepers", "Sleepers"),
        ("Timber", "Timber"),
        ("Treated Timber", "Treated Timber"),
    )
    PRESENT_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="features",
        null=True,
        blank=True,
    )
    pool_present = models.CharField(
        _("Pool Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    pool_material = models.CharField(
        _("Material"),
        choices=POOL_MATERIAL_CHOICES,
        max_length=100,
        default="Concrete",
    )
    pool_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    registerd = models.CharField(
        _("Registered"),
        choices=REGISTERED_CHOICES,
        max_length=5,
        default="YES",
    )
    registeration_number = models.CharField(
        _("Registration Number"), max_length=30, null=True, blank=True
    )
    pool_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    fencing_material = models.CharField(
        _("Material"),
        choices=FENCING_MATERIAL_CHOICES,
        max_length=100,
        default="Brick",
    )
    fencing_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    fencing_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    deck_present = models.CharField(
        _("Deck Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    deck_material = models.CharField(
        _("Material"),
        choices=DECK_MATERIAL_CHOICES,
        max_length=100,
        default="Concrete",
    )
    deck_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    deck_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    deck_length = models.IntegerField(_("Length"), null=True, blank=True)
    deck_width = models.IntegerField(_("Width"), null=True, blank=True)
    deck_height = models.IntegerField(_("Height"), null=True, blank=True)
    retaining_walls_material = models.CharField(
        _("Retaining Walls"),
        choices=RETAINING_WALLS_CHOICES,
        max_length=100,
        default="Blocks",
    )
    retaining_walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    retaining_walls_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )


class GrannyFlat(models.Model):
    LEVELS_CHOICES = (("1", "1"), ("2", "2"), ("3", "3"))
    FOUNDATION_CHOICES = (
        ("None", "None"),
        ("Piers", "Piers"),
        ("Pole", "Pole"),
        ("Slab", "Slab"),
    )
    WALLS_CHOICES = (
        ("None", "None"),
        ("Brick", "Brick"),
        ("Brick-Glass", "Brick-Glass"),
        ("Fibre Cement", "Fibre Cement"),
        ("Gyprock", "Gyprock"),
        ("Picture Rails", "Picture Rails"),
        ("Render", "Render"),
        ("Tiles", "Tiles"),
        ("Timber", "Timber"),
        ("Wall Paper", "Wall Paper"),
    )
    ROOF_DESCRIPTION_CHOICES = (
        ("None", "None"),
        ("Colourbond", "Colourbond"),
        ("Cliplock", "Cliplock"),
        ("Concrete Tile", "Concrete Tile"),
        ("Decromastic", "Decromastic"),
        ("Other", "Other"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    PRESENT_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name="granny_flat",
        null=True,
        blank=True,
    )
    granny_foundation_description = models.CharField(
        _("Foundation"),
        choices=FOUNDATION_CHOICES,
        max_length=100,
        default="Piers",
    )
    granny_foundation_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    granny_foundation_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    granny_walls_description = models.CharField(
        _("Description"),
        choices=WALLS_CHOICES,
        max_length=100,
        default="Brick",
    )
    granny_walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    granny_walls_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    granny_roof_description = models.CharField(
        _("Description"),
        choices=ROOF_DESCRIPTION_CHOICES,
        max_length=100,
        default="Colourbond",
    )
    granny_roof_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=100,
        default="Excellent",
    )
    granny_roof_comments = models.CharField(
        _("Comments"), max_length=300, null=True, blank=True
    )
    building_area = models.IntegerField(
        _("Building Area"), null=True, blank=True
    )
    carport_area = models.IntegerField(
        _("Carport Area"), null=True, blank=True
    )
    garage_area = models.IntegerField(_("Garage Area"), null=True, blank=True)
    is_granny_flat = models.CharField(
        _("Is There A Granny Flat"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )


# Internal details models for inspection sheet
class Entry(models.Model):
    FLOORS_CHOICES = (
        ("None", "None"),
        ("Carpet", "Carpet"),
        ("Carpet-Pattern", "Carpet-Pattern"),
        ("Carpet-Plain", "Carpet-Plain"),
        ("Concrete", "Concrete"),
        ("Cork", "Cork"),
        ("Plastic", "Plastic"),
        ("Plastic-Lino", "Plastic-Lino"),
        ("Plastic-Vinyl", "Plastic-Vinyl"),
        ("Stone", "Stone"),
        ("Stone-Granite", "Stone-Granite"),
        ("Stone-Limestone", "Stone-Limestone"),
        ("Stone-Marble", "Stone-Marble"),
        ("Stone-Sandstone", "Stone-Sandstone"),
        ("Stone-Slate", "Stone-Slate"),
        ("Stone-Travertine", "Stone-Travertine"),
        ("Stone-Terrazzo", "Stone-Terrazzo"),
        ("Tile", "Tile"),
        ("Tile-Ceramic", "Tile-Ceramic"),
        ("Tile-Mosaic", "Tile-Mosaic"),
        ("Tile-Porcelain", "Tile-Porcelain"),
        ("Tile-Wood", "Tile-Wood"),
        ("Timber", "Timber"),
        ("Timber-Floating Floor", "Timber-Floating Floor"),
        ("Timber-Hardwood", "Timber-Hardwood"),
        ("Timber-Polished", "Timber-Polished"),
    )
    CEILING_CHOICES = (
        ("None", "None"),
        ("Gyprock", "Gyprock"),
        ("Fibre Cement", "Fibre Cement"),
        ("Timber", "Timber"),
    )
    WALLS_CHOICES = (
        ("None", "None"),
        ("Brick", "Brick"),
        ("Brick-Glass", "Brick-Glass"),
        ("Fibre Cement", "Fibre Cement"),
        ("Gyprock", "Gyprock"),
        ("Picture Rails", "Picture Rails"),
        ("Render", "Render"),
        ("Tiles", "Tiles"),
        ("Timber", "Timber"),
        ("Wall Paper", "Wall Paper"),
    )
    LIGHT_FITTINGS_CHOICES = (
        ("None", "None"),
        ("Halogens", "Halogens"),
        ("Track", "Track"),
        ("Down Light", "Down Light"),
        ("Fluro", "Fluro"),
        ("LED", "LED"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    CURTAINS_OR_BLINDS_CHOICES = (
        ("None", "None"),
        ("Blinds", "Blinds"),
        ("Blinds-Aluminium", "Blinds-Aluminium"),
        ("Blinds-Honeycomb", "Blinds-Honeycomb"),
        ("Blinds-Mini", "Blinds-Mini"),
        ("Blinds-Panel", "Blinds-Panel"),
        ("Blinds-Pleated", "Blinds-Pleated"),
        ("Blinds-Roller", "Blinds-Roller"),
        ("Blinds-Sheer", "Blinds-Sheer"),
        ("Blinds-Venetian", "Blinds-Venetian"),
        ("Blinds-Vertical", "Blinds-Vertical"),
        ("Curtains", "Curtains"),
        ("Curtains-Box Pleated", "Curtains-Box Pleated"),
        ("Curtains-Eyelet", "Curtains-Eyelet"),
        ("Curtains-Goblet", "Curtains-Goblet"),
        ("Curtains-Tailored Pleat", "Curtains-Tailored Pleat"),
    )
    PRESENT_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True, blank=True
    )
    granny_flat = models.OneToOneField(
        GrannyFlat,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="entry",
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    floors = models.CharField(
        _("Floors"), choices=FLOORS_CHOICES, max_length=50, default="Carpet"
    )
    floors_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    floors_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    ceiling = models.CharField(
        _("Ceiling"), choices=CEILING_CHOICES, max_length=50, default="Gyprock"
    )
    ceiling_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    ceiling_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    walls = models.CharField(
        _("Walls"), choices=WALLS_CHOICES, max_length=50, default="Brick"
    )
    walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    walls_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    light_fittings = models.CharField(
        _("Light Fittings"),
        choices=LIGHT_FITTINGS_CHOICES,
        max_length=50,
        default="Halogens",
    )
    light_fittings_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    window_present = models.CharField(
        _("Window Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    window_length = models.IntegerField(_("Length"), null=True, blank=True)
    window_width = models.IntegerField(_("Width"), null=True, blank=True)
    window_height = models.IntegerField(_("Height"), null=True, blank=True)
    sliding_door_present = models.CharField(
        _("Sliding Door Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    sliding_door_length = models.IntegerField(
        _("Length"), null=True, blank=True
    )
    sliding_door_width = models.IntegerField(_("Width"), null=True, blank=True)
    sliding_door_height = models.IntegerField(
        _("Height"), null=True, blank=True
    )
    curtains_or_blinds = models.CharField(
        _("Curtains/Blinds"),
        choices=CURTAINS_OR_BLINDS_CHOICES,
        max_length=50,
        default="Blinds",
    )
    curtains_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )


class Lounge(models.Model):
    FLOORS_CHOICES = (
        ("None", "None"),
        ("Carpet", "Carpet"),
        ("Carpet-Pattern", "Carpet-Pattern"),
        ("Carpet-Plain", "Carpet-Plain"),
        ("Concrete", "Concrete"),
        ("Cork", "Cork"),
        ("Plastic", "Plastic"),
        ("Plastic-Lino", "Plastic-Lino"),
        ("Plastic-Vinyl", "Plastic-Vinyl"),
        ("Stone", "Stone"),
        ("Stone-Granite", "Stone-Granite"),
        ("Stone-Limestone", "Stone-Limestone"),
        ("Stone-Marble", "Stone-Marble"),
        ("Stone-Sandstone", "Stone-Sandstone"),
        ("Stone-Slate", "Stone-Slate"),
        ("Stone-Travertine", "Stone-Travertine"),
        ("Stone-Terrazzo", "Stone-Terrazzo"),
        ("Tile", "Tile"),
        ("Tile-Ceramic", "Tile-Ceramic"),
        ("Tile-Mosaic", "Tile-Mosaic"),
        ("Tile-Porcelain", "Tile-Porcelain"),
        ("Tile-Wood", "Tile-Wood"),
        ("Timber", "Timber"),
        ("Timber-Floating Floor", "Timber-Floating Floor"),
        ("Timber-Hardwood", "Timber-Hardwood"),
        ("Timber-Polished", "Timber-Polished"),
    )
    CEILING_CHOICES = (
        ("None", "None"),
        ("Gyprock", "Gyprock"),
        ("Fibre Cement", "Fibre Cement"),
        ("Timber", "Timber"),
    )
    WALLS_CHOICES = (
        ("None", "None"),
        ("Brick", "Brick"),
        ("Brick-Glass", "Brick-Glass"),
        ("Fibre Cement", "Fibre Cement"),
        ("Gyprock", "Gyprock"),
        ("Picture Rails", "Picture Rails"),
        ("Render", "Render"),
        ("Tiles", "Tiles"),
        ("Timber", "Timber"),
        ("Wall Paper", "Wall Paper"),
    )
    LIGHT_FITTINGS_CHOICES = (
        ("Halogens", "Halogens"),
        ("Track", "Track"),
        ("Down Light", "Down Light"),
        ("Fluro", "Fluro"),
        ("LED", "LED"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    CURTAINS_OR_BLINDS_CHOICES = (
        ("None", "None"),
        ("Blinds", "Blinds"),
        ("Blinds-Aluminium", "Blinds-Aluminium"),
        ("Blinds-Honeycomb", "Blinds-Honeycomb"),
        ("Blinds-Mini", "Blinds-Mini"),
        ("Blinds-Panel", "Blinds-Panel"),
        ("Blinds-Pleated", "Blinds-Pleated"),
        ("Blinds-Roller", "Blinds-Roller"),
        ("Blinds-Sheer", "Blinds-Sheer"),
        ("Blinds-Venetian", "Blinds-Venetian"),
        ("Blinds-Vertical", "Blinds-Vertical"),
        ("Curtains", "Curtains"),
        ("Curtains-Box Pleated", "Curtains-Box Pleated"),
        ("Curtains-Eyelet", "Curtains-Eyelet"),
        ("Curtains-Goblet", "Curtains-Goblet"),
        ("Curtains-Tailored Pleat", "Curtains-Tailored Pleat"),
    )
    PRESENT_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True, blank=True
    )
    granny_flat = models.OneToOneField(
        GrannyFlat,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="lounge",
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    floors = models.CharField(
        _("Floors"), choices=FLOORS_CHOICES, max_length=50, default="Carpet"
    )
    floors_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    floors_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    ceiling = models.CharField(
        _("Ceiling"), choices=CEILING_CHOICES, max_length=50, default="Gyprock"
    )
    ceiling_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    ceiling_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    walls = models.CharField(
        _("Walls"), choices=WALLS_CHOICES, max_length=50, default="Brick"
    )
    walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    walls_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    light_fittings = models.CharField(
        _("Light Fittings"),
        choices=LIGHT_FITTINGS_CHOICES,
        max_length=50,
        default="Halogens",
    )
    light_fittings_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    room_length = models.IntegerField(_("Length"), null=True, blank=True)
    room_width = models.IntegerField(_("Width"), null=True, blank=True)
    room_height = models.IntegerField(_("Height"), null=True, blank=True)
    window_length = models.IntegerField(_("Length"), null=True, blank=True)
    window_width = models.IntegerField(_("Width"), null=True, blank=True)
    window_height = models.IntegerField(_("Height"), null=True, blank=True)
    balcony_present = models.CharField(
        _("Balcony Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    balcony_length = models.IntegerField(_("Length"), null=True, blank=True)
    balcony_width = models.IntegerField(_("Width"), null=True, blank=True)
    balcony_height = models.IntegerField(_("Height"), null=True, blank=True)
    sliding_door_present = models.CharField(
        _("Sliding Door Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    sliding_door_length = models.IntegerField(
        _("Length"), null=True, blank=True
    )
    sliding_door_width = models.IntegerField(_("Width"), null=True, blank=True)
    sliding_door_height = models.IntegerField(
        _("Height"), null=True, blank=True
    )
    curtains_or_blinds = models.CharField(
        _("Curtains/Blinds"),
        choices=CURTAINS_OR_BLINDS_CHOICES,
        max_length=50,
        default="Blinds",
    )
    curtains_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    # Features fields
    air_conditioning_ducted = models.BooleanField(
        _("Air Conditioning-Ducted"), default=False
    )
    air_conditioning_wall_mounted = models.BooleanField(
        _("Air Conditioning-Wall Mounted"), default=False
    )
    ceiling_fan = models.BooleanField(_("Ceiling Fan"), default=False)
    ducted_vacuum = models.BooleanField(_("Ducted Vacuum"), default=False)
    exposed_timber_beams = models.BooleanField(
        _("Exposed Timber Beams"), default=False
    )
    fire_place_combustion = models.BooleanField(
        _("Fire Place - Combustion"), default=False
    )
    fire_place_gas = models.BooleanField(_("Fire Place - Gas"), default=False)
    intercom_system = models.BooleanField(_("Intercom System"), default=False)
    sky_light = models.BooleanField(_("Sky Light"), default=False)
    tv_outlet = models.BooleanField(_("TV Outlet"), default=False)
    wet_bar = models.BooleanField(_("Wet Bar"), default=False)


class Dining(models.Model):
    FLOORS_CHOICES = (
        ("None", "None"),
        ("Carpet", "Carpet"),
        ("Carpet-Pattern", "Carpet-Pattern"),
        ("Carpet-Plain", "Carpet-Plain"),
        ("Concrete", "Concrete"),
        ("Cork", "Cork"),
        ("Plastic", "Plastic"),
        ("Plastic-Lino", "Plastic-Lino"),
        ("Plastic-Vinyl", "Plastic-Vinyl"),
        ("Stone", "Stone"),
        ("Stone-Granite", "Stone-Granite"),
        ("Stone-Limestone", "Stone-Limestone"),
        ("Stone-Marble", "Stone-Marble"),
        ("Stone-Sandstone", "Stone-Sandstone"),
        ("Stone-Slate", "Stone-Slate"),
        ("Stone-Travertine", "Stone-Travertine"),
        ("Stone-Terrazzo", "Stone-Terrazzo"),
        ("Tile", "Tile"),
        ("Tile-Ceramic", "Tile-Ceramic"),
        ("Tile-Mosaic", "Tile-Mosaic"),
        ("Tile-Porcelain", "Tile-Porcelain"),
        ("Tile-Wood", "Tile-Wood"),
        ("Timber", "Timber"),
        ("Timber-Floating Floor", "Timber-Floating Floor"),
        ("Timber-Hardwood", "Timber-Hardwood"),
        ("Timber-Polished", "Timber-Polished"),
    )
    CEILING_CHOICES = (
        ("None", "None"),
        ("Gyprock", "Gyprock"),
        ("Fibre Cement", "Fibre Cement"),
        ("Timber", "Timber"),
    )
    WALLS_CHOICES = (
        ("None", "None"),
        ("Brick", "Brick"),
        ("Brick-Glass", "Brick-Glass"),
        ("Fibre Cement", "Fibre Cement"),
        ("Gyprock", "Gyprock"),
        ("Picture Rails", "Picture Rails"),
        ("Render", "Render"),
        ("Tiles", "Tiles"),
        ("Timber", "Timber"),
        ("Wall Paper", "Wall Paper"),
    )
    LIGHT_FITTINGS_CHOICES = (
        ("Halogens", "Halogens"),
        ("Track", "Track"),
        ("Down Light", "Down Light"),
        ("Fluro", "Fluro"),
        ("LED", "LED"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    CURTAINS_OR_BLINDS_CHOICES = (
        ("None", "None"),
        ("Blinds", "Blinds"),
        ("Blinds-Aluminium", "Blinds-Aluminium"),
        ("Blinds-Honeycomb", "Blinds-Honeycomb"),
        ("Blinds-Mini", "Blinds-Mini"),
        ("Blinds-Panel", "Blinds-Panel"),
        ("Blinds-Pleated", "Blinds-Pleated"),
        ("Blinds-Roller", "Blinds-Roller"),
        ("Blinds-Sheer", "Blinds-Sheer"),
        ("Blinds-Venetian", "Blinds-Venetian"),
        ("Blinds-Vertical", "Blinds-Vertical"),
        ("Curtains", "Curtains"),
        ("Curtains-Box Pleated", "Curtains-Box Pleated"),
        ("Curtains-Eyelet", "Curtains-Eyelet"),
        ("Curtains-Goblet", "Curtains-Goblet"),
        ("Curtains-Tailored Pleat", "Curtains-Tailored Pleat"),
    )
    PRESENT_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True, blank=True
    )
    granny_flat = models.OneToOneField(
        GrannyFlat,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dining",
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    floors = models.CharField(
        _("Floors"), choices=FLOORS_CHOICES, max_length=50, default="Carpet"
    )
    floors_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    floors_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    ceiling = models.CharField(
        _("Ceiling"), choices=CEILING_CHOICES, max_length=50, default="Gyprock"
    )
    ceiling_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    ceiling_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    walls = models.CharField(
        _("Walls"), choices=WALLS_CHOICES, max_length=50, default="Brick"
    )
    walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    walls_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    light_fittings = models.CharField(
        _("Light Fittings"),
        choices=LIGHT_FITTINGS_CHOICES,
        max_length=50,
        default="Halogens",
    )
    light_fittings_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    room_length = models.IntegerField(_("Length"), null=True, blank=True)
    room_width = models.IntegerField(_("Width"), null=True, blank=True)
    room_height = models.IntegerField(_("Height"), null=True, blank=True)
    window_length = models.IntegerField(_("Length"), null=True, blank=True)
    window_width = models.IntegerField(_("Width"), null=True, blank=True)
    window_height = models.IntegerField(_("Height"), null=True, blank=True)
    balcony_present = models.CharField(
        _("Balcony Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    balcony_length = models.IntegerField(_("Length"), null=True, blank=True)
    balcony_width = models.IntegerField(_("Width"), null=True, blank=True)
    balcony_height = models.IntegerField(_("Height"), null=True, blank=True)
    sliding_door_present = models.CharField(
        _("Sliding Door Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    sliding_door_length = models.IntegerField(
        _("Length"), null=True, blank=True
    )
    sliding_door_width = models.IntegerField(_("Width"), null=True, blank=True)
    sliding_door_height = models.IntegerField(
        _("Height"), null=True, blank=True
    )
    curtains_or_blinds = models.CharField(
        _("Curtains/Blinds"),
        choices=CURTAINS_OR_BLINDS_CHOICES,
        max_length=50,
        default="Blinds",
    )
    curtains_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    # Features fields
    air_conditioning_ducted = models.BooleanField(
        _("Air Conditioning-Ducted"), default=False
    )
    air_conditioning_wall_mounted = models.BooleanField(
        _("Air Conditioning-Wall Mounted"), default=False
    )
    ceiling_fan = models.BooleanField(_("Ceiling Fan"), default=False)
    ducted_vacuum = models.BooleanField(_("Ducted Vacuum"), default=False)
    exposed_timber_beams = models.BooleanField(
        _("Exposed Timber Beams"), default=False
    )
    fire_place_combustion = models.BooleanField(
        _("Fire Place - Combustion"), default=False
    )
    fire_place_gas = models.BooleanField(_("Fire Place - Gas"), default=False)
    intercom_system = models.BooleanField(_("Intercom System"), default=False)
    sky_light = models.BooleanField(_("Sky Light"), default=False)
    tv_outlet = models.BooleanField(_("TV Outlet"), default=False)
    wet_bar = models.BooleanField(_("Wet Bar"), default=False)


class Kitchen(models.Model):
    BENCH_TOPS_CHOICES = (
        ("None", "None"),
        ("Ceaser Stone", "Ceaser Stone"),
        ("Concrete", "Concrete"),
        ("Granite", "Granite"),
        ("Laminated", "Laminated"),
        ("Quartz", "Quartz"),
        ("Stainless Steel", "Stainless Steel"),
        ("Stone", "Stone"),
        ("Timber", "Timber"),
    )
    COOKTOP_CHOICES = (
        ("None", "None"),
        ("Electric", "Electric"),
        ("Gas", "Gas"),
    )
    COOKTOP_VENTILATION_CHOICES = (
        ("None", "None"),
        ("Exhaust Fan", "Exhaust Fan"),
        ("Rangehood", "Rangehood"),
    )
    CUPBOARDS_CHOICES = (
        ("None", "None"),
        ("Laminated", "Laminated"),
        ("Timber", "Timber"),
        ("Polyurethane", "Polyurethane"),
    )
    OVEN_OR_STOVE_CHOICES = (
        ("None", "None"),
        ("Electric Upright", "Electric Upright"),
        ("Gas Upright", "Gas Upright"),
        ("Under Bench", "Under Bench"),
    )
    SINK_CHOICES = (
        ("None", "None"),
        ("Single", "Single"),
        ("1.25", "1.25"),
        ("1.50", "1.50"),
        ("Double", "Double"),
    )
    SPLASHBACK_CHOICES = (
        ("None", "None"),
        ("Ceramic Tile", "Ceramic Tile"),
        ("Glass", "Glass"),
        ("Glass Mosaic", "Glass Mosaic"),
        ("Stainless Steel", "Stainless Steel"),
        ("Stone", "Stone"),
        ("Other", "Other"),
    )
    PANTRY_CHOICES = (
        ("None", "None"),
        ("Built In", "Built In"),
        ("Walk In", "Walk In"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="kitchen",
    )
    granny_flat = models.OneToOneField(
        GrannyFlat,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="kitchen",
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    benchtops = models.CharField(
        _("Benchtops"),
        choices=BENCH_TOPS_CHOICES,
        max_length=50,
        default="Ceaser Stone",
    )
    cooktop = models.CharField(
        _("Cooktop"),
        choices=COOKTOP_CHOICES,
        max_length=50,
        default="Electric",
    )
    cooktop_ventilation = models.CharField(
        _("Cooktop Ventilation"),
        choices=COOKTOP_VENTILATION_CHOICES,
        max_length=50,
        default="Exhaust Fan",
    )
    cupboards = models.CharField(
        _("Cupboards"),
        choices=CUPBOARDS_CHOICES,
        max_length=50,
        default="Laminated",
    )
    kitchen_length = models.IntegerField(_("Length"), null=True, blank=True)
    kitchen_width = models.IntegerField(_("Width"), null=True, blank=True)
    kitchen_height = models.IntegerField(_("Height"), null=True, blank=True)
    oven_or_stove = models.CharField(
        _("Oven Or Stove"),
        choices=OVEN_OR_STOVE_CHOICES,
        max_length=50,
        default="Built In Micro",
    )
    sink = models.CharField(
        _("Sink"), choices=SINK_CHOICES, max_length=50, default="Single"
    )
    sink_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    splashback = models.CharField(
        _("Splashback"),
        choices=SPLASHBACK_CHOICES,
        max_length=50,
        default="Ceramic Tile",
    )
    pantry = models.CharField(
        _("Pantry"), choices=PANTRY_CHOICES, max_length=50, default="Built In"
    )
    # Features fields
    insinkerator = models.BooleanField(_("Insinkerator"), default=False)
    built_in_micro = models.BooleanField(_("Built-In Micro"), default=False)


class Laundry(models.Model):
    TUB_CHOICES = (
        ("None", "None"),
        ("Acrylic", "Acrylic"),
        ("Stainless Steel", "Stainless Steel"),
    )
    BENCH_CHOICES = (
        ("None", "None"),
        ("Laminated", "Laminated"),
        ("Timber", "Timber"),
    )
    _property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="laundry",
    )
    granny_flat = models.OneToOneField(
        GrannyFlat,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="laundry",
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    tub = models.CharField(
        _("Tub"), choices=TUB_CHOICES, max_length=50, default="Acrylic"
    )
    bench = models.CharField(
        _("Bench"), choices=BENCH_CHOICES, max_length=50, default="Laminated"
    )
    laundry_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )


class Bathroom(models.Model):
    BATH_CHOICES = (
        ("None", "None"),
        ("Single", "Single"),
        ("Spa", "Spa"),
        ("Other", "Other"),
    )
    HAND_BASIN_CHOICES = (
        ("None", "None"),
        ("Upright Ceramic", "Upright Ceramic"),
        ("Other", "Other"),
    )
    SHOWER_CHOICES = (
        ("None", "None"),
        ("Over Bath", "Over Bath"),
        ("Recess", "Recess"),
    )
    TOILET_CHOICES = (
        ("None", "None"),
        ("Dual Flush", "Dual Flush"),
        ("Single Flush", "Single Flush"),
    )
    VANITY_CHOICES = (
        ("None", "None"),
        ("Single", "Single"),
        ("Double", "Double"),
    )
    _property = models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True, blank=True
    )
    granny_flat = models.ForeignKey(
        GrannyFlat, on_delete=models.CASCADE, null=True, blank=True
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    bath = models.CharField(
        _("Bath"), choices=BATH_CHOICES, max_length=50, default="Single"
    )
    hand_basin = models.CharField(
        _("Hand Basin"),
        choices=HAND_BASIN_CHOICES,
        max_length=50,
        default="Upright Ceramic",
    )
    shower = models.CharField(
        _("Shower"), choices=SHOWER_CHOICES, max_length=50, default="Over Bath"
    )
    toilet = models.CharField(
        _("Toilet"),
        choices=TOILET_CHOICES,
        max_length=50,
        default="Dual Flush",
    )
    vanity = models.CharField(
        _("Vanity"), choices=VANITY_CHOICES, max_length=50, default="Single"
    )
    bathroom_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    bathroom_length = models.IntegerField(_("Length"), null=True, blank=True)
    bathroom_width = models.IntegerField(_("Width"), null=True, blank=True)
    bathroom_height = models.IntegerField(_("Height"), null=True, blank=True)


class Bedroom(models.Model):
    FLOORS_CHOICES = (
        ("None", "None"),
        ("Carpet", "Carpet"),
        ("Carpet-Pattern", "Carpet-Pattern"),
        ("Carpet-Plain", "Carpet-Plain"),
        ("Concrete", "Concrete"),
        ("Cork", "Cork"),
        ("Plastic", "Plastic"),
        ("Plastic-Lino", "Plastic-Lino"),
        ("Plastic-Vinyl", "Plastic-Vinyl"),
        ("Stone", "Stone"),
        ("Stone-Granite", "Stone-Granite"),
        ("Stone-Limestone", "Stone-Limestone"),
        ("Stone-Marble", "Stone-Marble"),
        ("Stone-Sandstone", "Stone-Sandstone"),
        ("Stone-Slate", "Stone-Slate"),
        ("Stone-Travertine", "Stone-Travertine"),
        ("Stone-Terrazzo", "Stone-Terrazzo"),
        ("Tile", "Tile"),
        ("Tile-Ceramic", "Tile-Ceramic"),
        ("Tile-Mosaic", "Tile-Mosaic"),
        ("Tile-Porcelain", "Tile-Porcelain"),
        ("Tile-Wood", "Tile-Wood"),
        ("Timber", "Timber"),
        ("Timber-Floating Floor", "Timber-Floating Floor"),
        ("Timber-Hardwood", "Timber-Hardwood"),
        ("Timber-Polished", "Timber-Polished"),
    )
    CEILING_CHOICES = (
        ("None", "None"),
        ("Gyprock", "Gyprock"),
        ("Fibre Cement", "Fibre Cement"),
        ("Timber", "Timber"),
    )
    WALLS_CHOICES = (
        ("None", "None"),
        ("Brick", "Brick"),
        ("Brick-Glass", "Brick-Glass"),
        ("Fibre Cement", "Fibre Cement"),
        ("Gyprock", "Gyprock"),
        ("Picture Rails", "Picture Rails"),
        ("Render", "Render"),
        ("Tiles", "Tiles"),
        ("Timber", "Timber"),
        ("Wall Paper", "Wall Paper"),
    )
    LIGHT_FITTINGS_CHOICES = (
        ("Halogens", "Halogens"),
        ("Track", "Track"),
        ("Down Light", "Down Light"),
        ("Fluro", "Fluro"),
        ("LED", "LED"),
    )
    CONDITION_CHOICES = (
        ("Excellent", "Excellent"),
        ("Above Average", "Above Average"),
        ("Average", "Average"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    )
    CURTAINS_OR_BLINDS_CHOICES = (
        ("None", "None"),
        ("Blinds", "Blinds"),
        ("Blinds-Aluminium", "Blinds-Aluminium"),
        ("Blinds-Honeycomb", "Blinds-Honeycomb"),
        ("Blinds-Mini", "Blinds-Mini"),
        ("Blinds-Panel", "Blinds-Panel"),
        ("Blinds-Pleated", "Blinds-Pleated"),
        ("Blinds-Roller", "Blinds-Roller"),
        ("Blinds-Sheer", "Blinds-Sheer"),
        ("Blinds-Venetian", "Blinds-Venetian"),
        ("Blinds-Vertical", "Blinds-Vertical"),
        ("Curtains", "Curtains"),
        ("Curtains-Box Pleated", "Curtains-Box Pleated"),
        ("Curtains-Eyelet", "Curtains-Eyelet"),
        ("Curtains-Goblet", "Curtains-Goblet"),
        ("Curtains-Tailored Pleat", "Curtains-Tailored Pleat"),
    )
    PRESENT_CHOICES = (("Yes", "Yes"), ("No", "No"))
    _property = models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True, blank=True
    )
    granny_flat = models.ForeignKey(
        GrannyFlat, on_delete=models.CASCADE, null=True, blank=True
    )
    location_name = models.CharField(
        _("Location Name"), max_length=50, null=True, blank=True
    )
    floors = models.CharField(
        _("Floors"), choices=FLOORS_CHOICES, max_length=50, default="Carpet"
    )
    floors_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    floors_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    ceiling = models.CharField(
        _("Ceiling"), choices=CEILING_CHOICES, max_length=50, default="Gyprock"
    )
    ceiling_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    ceiling_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    walls = models.CharField(
        _("Walls"), choices=WALLS_CHOICES, max_length=50, default="Brick"
    )
    walls_condition = models.CharField(
        _("Condition"),
        choices=CONDITION_CHOICES,
        max_length=50,
        default="Excellent",
    )
    walls_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    light_fittings = models.CharField(
        _("Light Fittings"),
        choices=LIGHT_FITTINGS_CHOICES,
        max_length=50,
        default="Halogens",
    )
    light_fittings_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    room_length = models.IntegerField(_("Length"), null=True, blank=True)
    room_width = models.IntegerField(_("Width"), null=True, blank=True)
    room_height = models.IntegerField(_("Height"), null=True, blank=True)
    window_length = models.IntegerField(_("Length"), null=True, blank=True)
    window_width = models.IntegerField(_("Width"), null=True, blank=True)
    window_height = models.IntegerField(_("Height"), null=True, blank=True)
    balcony_present = models.CharField(
        _("Balcony Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    balcony_length = models.IntegerField(_("Length"), null=True, blank=True)
    balcony_width = models.IntegerField(_("Width"), null=True, blank=True)
    balcony_height = models.IntegerField(_("Height"), null=True, blank=True)
    sliding_door_present = models.CharField(
        _("Sliding Door Present"),
        max_length=20,
        choices=PRESENT_CHOICES,
        default="Yes",
    )
    sliding_door_length = models.IntegerField(
        _("Length"), null=True, blank=True
    )
    sliding_door_width = models.IntegerField(_("Width"), null=True, blank=True)
    sliding_door_height = models.IntegerField(
        _("Height"), null=True, blank=True
    )
    curtains_or_blinds = models.CharField(
        _("Curtains/Blinds"),
        choices=CURTAINS_OR_BLINDS_CHOICES,
        max_length=50,
        default="Blinds",
    )
    curtains_comments = models.CharField(
        _("Comments"), max_length=50, null=True, blank=True
    )
    # Features fields
    air_conditioning_ducted = models.BooleanField(
        _("Air Conditioning-Ducted"), default=False
    )
    air_conditioning_wall_mounted = models.BooleanField(
        _("Air Conditioning-Wall Mounted"), default=False
    )
    ceiling_fan = models.BooleanField(_("Ceiling Fan"), default=False)
    ducted_vacuum = models.BooleanField(_("Ducted Vacuum"), default=False)
    ensuite = models.BooleanField(_("Ensuite"), default=False)
    tv_outlet = models.BooleanField(_("TV Outlet"), default=False)
    wardrobe_built_in = models.BooleanField(
        _("Wardrobe Built In"), default=False
    )
    wardrobe_walk_in = models.BooleanField(
        _("Wardrobe Walk In"), default=False
    )


# Create a signal when a new property is created. The inspection object and all the associated
# objects should be created and should be linked with the property object
# A granny flat is associated with each property. A granny flat also has it's own set of internal
# features such as entry, bedrooms, etc.
@receiver(post_save, sender=Property)
def signal_on_property_creation(sender, **kwargs):
    if kwargs["created"] is True:
        property_object = kwargs["instance"]
        # Create a granny flat object.
        granny_flat_object = GrannyFlat.objects.create(
            _property=property_object
        )

        # Creating objects for grany flat
        Entry.objects.create(granny_flat=granny_flat_object)
        Lounge.objects.create(granny_flat=granny_flat_object)
        Dining.objects.create(granny_flat=granny_flat_object)
        Kitchen.objects.create(granny_flat=granny_flat_object)
        Laundry.objects.create(granny_flat=granny_flat_object)

        # Creating 3 bedrooms and 3 bathrooms for a granny flat. If there are more bedrooms or
        # bathrooms, the user can mention them in comments
        for _counter in range(3):
            Bedroom.objects.create(granny_flat=granny_flat_object)
            Bathroom.objects.create(granny_flat=granny_flat_object)

        # Creating objects for internal property
        LandDetails.objects.create(_property=property_object)
        Zoning.objects.create(_property=property_object)
        Shape.objects.create(_property=property_object)
        StreetAppeal.objects.create(_property=property_object)
        Construction.objects.create(_property=property_object)
        Parking.objects.create(
            _property=property_object, location_name="Parking"
        )
        Features.objects.create(_property=property_object)

        Entry.objects.create(_property=property_object, location_name="Entry")
        Lounge.objects.create(
            _property=property_object, location_name="Lounge"
        )
        Dining.objects.create(
            _property=property_object, location_name="Dining"
        )
        Kitchen.objects.create(
            _property=property_object, location_name="Kitchen"
        )
        Laundry.objects.create(
            _property=property_object, location_name="Laundry"
        )

        # Number of bedrooms and bathrooms are asked from the user at the time of creation of leads
        number_of_bedrooms = property_object.beds
        if number_of_bedrooms:
            for _counter in range(number_of_bedrooms):
                Bedroom.objects.create(
                    _property=property_object, location_name="Bedroom"
                )
        else:  # Create one bedroom object
            Bedroom.objects.create(
                _property=property_object, location_name="Bedroom"
            )

        number_of_bathrooms = property_object.bath
        if number_of_bathrooms:
            for _counter in range(number_of_bathrooms):
                Bathroom.objects.create(
                    _property=property_object, location_name="Bathroom"
                )
        else:  # Create one bathroom object
            Bathroom.objects.create(
                _property=property_object, location_name="Bathroom"
            )
