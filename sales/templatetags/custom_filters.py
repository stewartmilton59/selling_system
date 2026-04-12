from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    """Subtract arg from value"""
    try:
        return value - arg
    except (ValueError, TypeError):
        return value


@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return value


@register.filter
def div(value, arg):
    """Divide value by arg"""
    try:
        if arg:
            return value / arg
        return 0
    except (ValueError, TypeError):
        return value


@register.filter
def add_tax(value, tax_rate=0.08):
    """Add tax to value (default 8%)"""
    try:
        return value + (value * tax_rate)
    except (ValueError, TypeError):
        return value
