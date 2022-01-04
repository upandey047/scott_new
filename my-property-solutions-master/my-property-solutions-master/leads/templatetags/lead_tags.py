from django import template

register = template.Library()


@register.simple_tag
def subtract_list_prices(var, arg):
    """
    This template tag is used to find the difference between the start list price and end list price.
    """
    if var is None and arg is None:
        return ""
    elif var is None or arg is None:
        return arg
    else:
        return var - arg


@register.simple_tag
def percentage_drop_list_price(var, arg):
    """
    This template tag is used to find the percentage drop between the start list price and end list price.
    """
    if var is None or arg is None:
        return ""
    else:
        return (var - arg) / 100


@register.filter
def filter_contact(obj, category):
    """
    Tag to filter contacts with respect of categories
    """
    return obj.property.contact_set.all().filter(category=category).first()
