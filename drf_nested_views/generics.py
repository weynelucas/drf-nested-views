from django.utils.functional import cached_property

from rest_framework.serializers import ModelSerializer
from rest_framework import generics
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


class GenericAPIView(generics.GenericAPIView):
    """
    Base class for all other generic views that are nested.
    """
    parent_lookup_kwargs = {}

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.

        If `serializer_class` attribute is a ModelSerializer 
        subclass, the queryset will be retrieved through 
        `model` attribute.
        """
        if issubclass(self.serializer_class, ModelSerializer):
            return self.serializer_class.Meta.model.objects.all()
        return super(GenericAPIView, self).get_queryset()

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

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter 
        backend is in use.
        
        After filter backend process, filter it with 
        `parent_lookup_kwargs` attribute.
        """
        queryset = super(GenericAPIView, self).filter_queryset(queryset)
        return queryset.filter(**self.get_parent_lookup())