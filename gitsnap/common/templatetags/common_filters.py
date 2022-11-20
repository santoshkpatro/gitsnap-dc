from django import template

register = template.Library()


@register.filter
def shrink_num(value):
    """
    Shrinks number rounding
    123456  > 123,5K
    123579  > 123,6K
    1234567 > 1,2M
    """
    value = str(value)

    if value.isdigit():
        value_int = int(value)

        if value_int >= 1000000:
            value = "%.0f%s" % (value_int / 1000000.00, "M")
        else:
            if value_int >= 1000:
                value = "%.0f%s" % (value_int / 1000.0, "k")
    return value
