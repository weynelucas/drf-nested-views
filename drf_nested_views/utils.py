from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import RelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import GenericAPIView


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


def get_view_queryset(view):
    """
    Get the list of items for this view from `queryset` or
    `serializer_class`.

    When the view not provide a `queryset`, the list of items will be 
    retrieved through `serializer_class`, if it is a ModelSerializer
    subclass. 
    """
    assert isinstance(view, GenericAPIView), (
        "'%s' must be an instance of GenericAPIView." %
        (str(view))
    )

    get_from_super = (
        view.queryset is not None or
        issubclass(view.serializer_class, ModelSerializer) is not True
    )

    if get_from_super:
        return super(view.__class__, view).get_queryset()
    
    return view.serializer_class.Meta.model.objects.all()