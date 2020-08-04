from django.template import Library

register = Library()


@register.filter
def get(item, attr):
    if hasattr(item, attr):
        return getattr(item, attr)
    else:
        return item

@register.filter
def flat(item):
    if hasattr(item, 'all'):
        result = item.all()
        return len(result)

    else:
        return item
