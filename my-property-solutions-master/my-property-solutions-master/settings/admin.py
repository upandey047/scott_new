from django.contrib import admin
from .models import (
    Address,
    RegisteredAddress,
    Email,
    Documents,
    Individual,
    Company,
    Shares,
    Trust,
    Entity,
    Category,
    Event,
    CheckList,
    DefaultCheckList,
)


admin.site.register(Address)
admin.site.register(RegisteredAddress)
admin.site.register(Email)
admin.site.register(Documents)
admin.site.register(Individual)
admin.site.register(Company)
admin.site.register(Shares)
admin.site.register(Trust)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(CheckList)
admin.site.register(DefaultCheckList)
