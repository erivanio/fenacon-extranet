from selectable.base import ModelLookup
from selectable.registry import registry

from apps.core.models import User


class UserLookup(ModelLookup):
    model = User
    search_fields = (
        'email__icontains',
        'first_name__icontains',
        'last_name__icontains',
        'job__icontains',
        'slug__icontains',
    )
    filters = {'is_active': True, }

    def get_item_value(self, item):
        # Display for currently selected item
        return item.get_short_name()

    def get_item_label(self, item):
        # Display for choice listings
        return u"%s" % (item.get_full_name())

registry.register(UserLookup)
