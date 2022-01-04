from django.contrib import admin
from .models import (
    Solicitor,
    Family,
    Executor,
    Other,
    Agent,
    BankNew,
    Liquidator,
    Deal,
    Purchase,
    PurchaseCosts,
    Sale,
    ProfitSplit,
    PurchaseComparableSales,
    SaleComparableSales,
    PurchaseComparableSalesImages,
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
    InternalTasksForMyself,
    ExternalTasksForMyself,
    HoldingCosts,
    FeasibilityReport,
    AFCAComplaintLodged,
)

# Register your models here.
admin.site.register(Solicitor)
admin.site.register(Agent)
admin.site.register(BankNew)
admin.site.register(Family)
admin.site.register(Other)
admin.site.register(Executor)
admin.site.register(Liquidator)
admin.site.register(Deal)
admin.site.register(Purchase)
admin.site.register(PurchaseCosts)
admin.site.register(HoldingCosts)
admin.site.register(FeasibilityReport)
admin.site.register(Sale)
admin.site.register(ProfitSplit)
admin.site.register(PurchaseComparableSales)
admin.site.register(SaleComparableSales)
admin.site.register(PurchaseComparableSalesImages)
admin.site.register(SaleComparableSalesImages)
admin.site.register(Renovation)
admin.site.register(Team)
admin.site.register(Rooms)
admin.site.register(Tasks)
admin.site.register(Images)
admin.site.register(MyPurchaseDetails)
admin.site.register(Materials)
admin.site.register(PrimeCostItems)
admin.site.register(PurchaseCorrespondanceDocuments)
admin.site.register(External)
admin.site.register(InternalTasksForMyself)
admin.site.register(ExternalTasksForMyself)
admin.site.register(AFCAComplaintLodged)