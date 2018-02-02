from django.http import Http404
from rest_framework.serializers import ModelSerializer
from rest_framework import generics
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .utils import (
    to_related_lookup,
)


class APIViewMixin(object):
    """
    Overrides `.get_queryset()` to get the list of items
    for a view.
    """
    def get_queryset(self):
        """
        Get the list of items for this view from `queryset` or
        `serializer_class`.

        When the view not provide a `queryset`, the list of items will be 
        retrieved through `serializer_class`, if it is a ModelSerializer
        subclass. 
        """
        get_from_super = (
            self.queryset is not None or
            issubclass(self.serializer_class, ModelSerializer) is not True
        )

        if get_from_super:
            return super(APIViewMixin, self).get_queryset()
        
        return self.serializer_class.Meta.model.objects.all()


class GenericAPIView(APIViewMixin, generics.GenericAPIView):
    """
    Base class for all other generic views that are nested.
    """
    parent_lookup_kwargs = {}

    def get_parent_lookup_kwargs(self):
        """
        Returns the parent lookup kwargs, a dictionary that maps
        URL parameters to object properties.
        Defaults to using `self.parent_lookup_kwargs`.

        If `serializer_class` attribute is a NestedHyperlinkedModelSerializer
        subclass, the kwargs will be retrieved from it through
        `parent_lookup_kwargs` attribute.
        """
        if issubclass(self.serializer_class, NestedHyperlinkedModelSerializer):
            return self.serializer_class.parent_lookup_kwargs
        
        assert self.parent_lookup_kwargs, (
            "'%s' should either include a `parent_lookup_kwargs` attribute, "
            "or override the `get_parent_lookup_kwargs()` method."
            % self.__class__.__name__
        )
        return self.parent_lookup_kwargs

    def get_parent_lookup(self):
        """
        Returns the entire lookup for parent based on `parent_lookup_kwargs`
        and URL keyword arguments.
        """
        parent_lookup_kwargs = self.get_parent_lookup_kwargs()
        try:
            return { v: self.kwargs[k] for k, v in parent_lookup_kwargs.items() }
        except KeyError as error:
            raise  AttributeError(
                "Keyword argument %s from `parent_lookup_kwargs` does not " 
                "have any match on URL keyword arguments."
                % str(error)
            )
    
    def get_parent_object(self):
        """
        Returns the parent object the view is displaying. 

        You may want override this if you need to provide non-standart
        queryset lookup.
        """
        model = self.get_queryset().model
        parent_lookup = self.get_parent_lookup()

        related_fields = list(set(
            [ k.split('__', 1)[0] for k in parent_lookup.keys() ]
        ))

        assert len(related_fields) == 1, (
            'Expected only one related field from `get_parent_lookup()`.' 
            'Got %s'  % 
            (len(related_fields))
        )

        related_field = related_fields[0]
        related_lookup = to_related_lookup(model, parent_lookup)
        related_model = model._meta.get_field(related_field).related_model

        assert related_model is not None, (
            "%s has no related field named '%s'." %
            (model.__name__, related_field)
        )
    
        try:
            return related_model.objects.get(**related_lookup)
        except related_model.DoesNotExist:
            raise Http404

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter 
        backend is in use.
        
        After filter backend process, filter it with 
        `parent_lookup_kwargs` attribute.
        """

        # Find parent resource object and raises 404 when not found
        self.get_parent_object()

        return super(GenericAPIView, self)       \
            .filter_queryset(queryset)           \
            .filter(**self.get_parent_lookup())
