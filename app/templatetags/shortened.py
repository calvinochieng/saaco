from django import template

register = template.Library()

@register.filter
def shorten_this(value):
    """
    Convert a large number into a more human-readable format.
    Examples:
    1000 -> '1k'
    1000000 -> '1m'
    1000000000 -> '1b'
    """
    try:
        value = int(value)
        if value >= 1_000_000_000:
            return f"{value // 1_000_000_000}b"
        elif value >= 1_000_000:
            return f"{value // 1_000_000}m"
        elif value >= 1_000:
            return f"{value // 1_000}k"
        else:
            return str(value)
    except (ValueError, TypeError):
        return value
