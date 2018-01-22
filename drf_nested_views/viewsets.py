from rest_framework.viewsets import ViewSetMixin

from . import mixins
from . import generics


class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The NestedGenericViewSet class does not provide any actions by default,
    but does include the base set of generic nested view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class ReadOnlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` nested actions.
    """
    pass


class ModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` nested actions.
    """
    pass