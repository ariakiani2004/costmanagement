from django import template

register = template.Library()
PERSIAN_DIGITS = str.maketrans("0123456789,", "۰۱۲۳۴۵۶۷۸۹٬")


@register.filter
def fa_digits(value):
    return str(value).translate(PERSIAN_DIGITS)


@register.filter
def money(value):
    return format(value, ",d").translate(PERSIAN_DIGITS)
