from django.contrib import admin
from .models import (
    Lead,
    Property,
    PropertyOwner,
    Bank,
    PersonalLoan,
    Title,
    Dealing,
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
    Auction,
)

# Register your models here.

admin.site.register(Lead)
admin.site.register(Property)
admin.site.register(PropertyOwner)
admin.site.register(Bank)
admin.site.register(PersonalLoan)
admin.site.register(Title)
admin.site.register(Dealing)
admin.site.register(LandDetails)
admin.site.register(Zoning)
admin.site.register(Shape)
admin.site.register(StreetAppeal)
admin.site.register(Construction)
admin.site.register(Parking)
admin.site.register(Features)
admin.site.register(GrannyFlat)
admin.site.register(Entry)
admin.site.register(Lounge)
admin.site.register(Dining)
admin.site.register(Kitchen)
admin.site.register(Laundry)
admin.site.register(Bathroom)
admin.site.register(Bedroom)
admin.site.register(Auction)
