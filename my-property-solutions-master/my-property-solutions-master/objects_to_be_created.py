from settings.models import Event, Category

Category.objects.create(category_name="initial_research")
Category.objects.create(category_name="letters")
Category.objects.create(category_name="inspection")
Category.objects.create(category_name="due_diligence")
Category.objects.create(category_name="property_searches")
Category.objects.create(category_name="market_research")
Category.objects.create(category_name="offer_or_finance")
Category.objects.create(category_name="exchange_or_settlement")
Category.objects.create(category_name="renovation")
Category.objects.create(category_name="listing_for_sale")
Category.objects.create(category_name="sale-exchange_or_settlement")

Event.objects.create(
    event_name="RP Data Search of Property", default_event=True
)
Event.objects.create(event_name="On The House.com.au", default_event=True)
Event.objects.create(event_name="Block Brief", default_event=True)
Event.objects.create(
    event_name="Real Estate.com.au - Stock on market", default_event=True
)
Event.objects.create(
    event_name="Real Estate.com.au - Stock Sold", default_event=True
)
Event.objects.create(event_name="DSR Score", default_event=True)
Event.objects.create(event_name="Send Letter 1 - Owner", default_event=True)
Event.objects.create(event_name="Send Letter 2 - Owner", default_event=True)
Event.objects.create(event_name="Send Letter 3 - Owner", default_event=True)
Event.objects.create(event_name="Send Letter 1 - Bank", default_event=True)
Event.objects.create(event_name="Send Letter 2 - Bank", default_event=True)
Event.objects.create(event_name="Send Letter 3 - Bank", default_event=True)
Event.objects.create(event_name="Send Letter 1 - Lawyer", default_event=True)
Event.objects.create(event_name="Send Letter 2 - Lawyer", default_event=True)
Event.objects.create(event_name="Send Letter 3 - Lawyer", default_event=True)
Event.objects.create(event_name="Inspection Organised", default_event=True)
Event.objects.create(event_name="Inspection Carried Out", default_event=True)
Event.objects.create(event_name="Inspection Sheet", default_event=True)
Event.objects.create(event_name="Interview Owner", default_event=True)
Event.objects.create(event_name="Photos", default_event=True)
Event.objects.create(
    event_name="Assess property at first glance", default_event=True
)
Event.objects.create(event_name="Assess Neighbourhood", default_event=True)
Event.objects.create(
    event_name="Research Subject Property Information", default_event=True
)
Event.objects.create(
    event_name="Professional Building Inspection", default_event=True
)
Event.objects.create(
    event_name="Professional Pest Inspection", default_event=True
)
Event.objects.create(event_name="Engineering Report", default_event=True)
Event.objects.create(event_name="Title Search", default_event=True)
Event.objects.create(event_name="Strata Search", default_event=True)
Event.objects.create(event_name="Encumbrance Search", default_event=True)
Event.objects.create(event_name="Building Record Search", default_event=True)
Event.objects.create(event_name="Flood Zone Search", default_event=True)
Event.objects.create(event_name="Bushfire Search", default_event=True)
Event.objects.create(event_name="Survey Report", default_event=True)
Event.objects.create(event_name="Contract For Sale", default_event=True)
Event.objects.create(event_name="Offer Created", default_event=True)
Event.objects.create(event_name="Offer Submitted", default_event=True)
Event.objects.create(event_name="Offer Accepted", default_event=True)
Event.objects.create(event_name="Offer Declined", default_event=True)
Event.objects.create(event_name="Terms of Agreement", default_event=True)
Event.objects.create(event_name="Engage Broker / Bank", default_event=True)
Event.objects.create(event_name="Pre Approval", default_event=True)
Event.objects.create(event_name="Formal Approval", default_event=True)
Event.objects.create(event_name="Engage Legal Team", default_event=True)
Event.objects.create(
    event_name="Prepare Contact - Legal Team", default_event=True
)
Event.objects.create(
    event_name="Engage Local Council for project requirements",
    default_event=True,
)
Event.objects.create(
    event_name="Engage Builder / Trades People", default_event=True
)
Event.objects.create(
    event_name="Engage Architect / Drafts Person", default_event=True
)
Event.objects.create(event_name="Engage Engineer", default_event=True)
Event.objects.create(event_name="Pay DA Fees", default_event=True)
Event.objects.create(event_name="Lodge DA", default_event=True)
Event.objects.create(
    event_name="Confirm Materials & PC Items", default_event=True
)
Event.objects.create(
    event_name="Determine Renovation Budget", default_event=True
)
Event.objects.create(event_name="Stock On Market", default_event=True)
Event.objects.create(event_name="Avg Days on Market", default_event=True)
Event.objects.create(event_name="Demographics", default_event=True)
Event.objects.create(event_name="Comparable Sales", default_event=True)
Event.objects.create(
    event_name="Deposit Paid - .25% - Cool Off Period", default_event=True
)
Event.objects.create(event_name="Deposit Paid - 10%", default_event=True)
Event.objects.create(
    event_name="Confirm Net Funds Available", default_event=True
)
Event.objects.create(event_name="Collect Keys", default_event=True)
Event.objects.create(event_name="Arrange Market Appraisal", default_event=True)
Event.objects.create(event_name="Engage Valuer", default_event=True)
Event.objects.create(event_name="Engage Agent", default_event=True)
Event.objects.create(
    event_name="Determine Minimum Sale Price", default_event=True
)
Event.objects.create(event_name="List Property For Sale", default_event=True)
Event.objects.create(
    event_name="Engage Legal Firm - Contract For Sale", default_event=True
)
Event.objects.create(
    event_name="Prepare Property For Sale", default_event=True
)
Event.objects.create(
    event_name="Negotiate Terms of Contract", default_event=True
)
Event.objects.create(event_name="Purchaser To Pay Deposit", default_event=True)
Event.objects.create(event_name="Exchange", default_event=True)
Event.objects.create(event_name="Settlement", default_event=True)
