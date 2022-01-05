from django import template
from deals.models import Deal, AFCAComplaintLodged

register = template.Library()


@register.simple_tag
def deal_owner_name(deal_id):
    """
    This template tag is used to find the deal info.
    """
    deal_obj = Deal.objects.get(pk=deal_id)
    property_owner = deal_obj.lead.property.property_owner.first()
    if property_owner.first_name is not None and property_owner.last_name is not None:
        return str(property_owner.first_name) + " " + str(property_owner.last_name)
    elif property_owner.first_name is None and property_owner.last_name is None:
        # print(property_owner.first_name,property_owner.last_name)
        return "--"
        
        


@register.simple_tag
def deal_property_address(deal_id):
    """
    This template tag is used to find the deal info.
    """
    deal_obj = Deal.objects.get(pk=deal_id)
    property_obj = deal_obj.lead.property
    unit = str(property_obj.unit) if property_obj.unit else ""
    number = str(property_obj.number) if property_obj.number else ""
    street = str(property_obj.street) if property_obj.street else ""
    suburb = str(property_obj.suburb) if property_obj.suburb else ""
    state = str(property_obj.state) if property_obj.state else ""
    post_code = str(property_obj.post_code) if property_obj.post_code else ""
    po_box = str(property_obj.po_box) if property_obj.po_box else ""
    return (
        unit
        + " "
        + number
        + " "
        + street
        + " "
        + suburb
        + " "
        + state
        + " "
        + post_code
        + " "
        + po_box
    )


@register.simple_tag
def afca_complaint_lodged(deal_id):
    """
    This template tag is used to find if AFCA Complaint is lodged or not
    """
    deal_obj = Deal.objects.get(pk=deal_id)
    complaint_lodged = AFCAComplaintLodged.objects.filter(deal=deal_obj)
    if complaint_lodged:
        return complaint_lodged.first().complaint_lodged_status
    else:
        return "No"
