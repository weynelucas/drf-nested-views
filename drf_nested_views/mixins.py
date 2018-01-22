"""
Basic building blocks for generic class based views.

Use theese mixins with GenericAPIView from drf_nested_views.

With exception of CreateModelMixin and UpdateModelMixin, 
other mixins does not perform or override any action of
his parents (rest_framework.mixins). Use them for track 
future changes.
"""
from rest_framework import mixins


class CreateModelMixin(mixins.CreateModelMixin):
    """
    Create a nested model instance.
    """
    def perform_create(self, serializer):
        serializer.save(**self.get_parent_lookup())


class ListModelMixin(mixins.ListModelMixin):
    """
    List a nested queryset.
    """
    pass


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    Retrieve a nested model instance.
    """
    pass


class UpdateModelMixin(mixins.UpdateModelMixin):
    """
    Update a nested model instance.
    """
    def perform_update(self, serializer):
        serializer.save(**self.get_parent_lookup())


class DestroyModelMixin(mixins.DestroyModelMixin):
    """
    Destroy a nested model instance.
    """
    pass