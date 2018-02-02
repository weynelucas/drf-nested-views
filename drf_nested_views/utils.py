from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import RelatedField


def to_related_lookup(base_model, lookup):
    """
    Convert a `lookup` query dictionary for `base_model`
    context into another query dictionary  for `related_model`
    context.

    This function transform `lookup` into a query dictionary
    that can be used to query for a related object.

    Example:
        from drf_nested_views.utils import to_related_lookup
        from recipients.models import Recipient

        relatd_lookup = to_related_lookup(
            base_model=Recipient, 
            lookup={ 'mail_drop_pk': 1, 'mail_drop__client_pk': 5 } 
        )

        print(related_lookup) # { 'pk': 1, 'client_pk': 5 }
    """
    normalized = {}
    for k, v in lookup.items():
        # Get related pk field
        try: 
            field = base_model._meta.get_field(k)
            if isinstance(field, RelatedField):
                k = field.related_model._meta.pk.name
        except FieldDoesNotExist:
            pass
        
        # Split from join delimitter
        normalized_key = k.split('__', 1)[-1]
        normalized[normalized_key] = v
    return normalized