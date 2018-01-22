# drf-nested-views
A set of views to work with [drf-nested-routers](https://github.com/alanjds/drf-nested-routers)


## Instalation
You can install this library using pip:

```
pip install drf-nested-views
```

## Requirements
This library was tested with the follow dependencies:

* [Django](https://www.djangoproject.com/) - 1.11
* [Django REST Framework](http://www.django-rest-framework.org/) - 3.7
* [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) - 0.90.0


## Quickstart
Configure your desired URL signatures:

```python
# urls.py
from rest_framework_nested import routers
from views import DomainViewSet, NameserverViewSet
(...)

router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet)

domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
domains_router.register(r'nameservers', NameserverViewSet, base_name='domain-nameservers')


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^', include(domains_router.urls)),
)
```

Configure serialization, with `NestedHyperlinkedModelSerializer` for nested objects:

```python
# serializers.py
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


class NameserverSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'domain_pk': 'domain__pk',
    }
    class Meta:
        model = Nameserver
        fields = ('url', ...)


class DomainSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Domain
	fields = (..., 'nameservers')

    nameservers = NameserverSerializer(many=True, read_only=True)
```

Create your viewsets extending `ModelViewSet` or `ReadOnlyModelViewSet` from `drf_nested_views.viewsets` to improve nested resources behaviour:

```python
# views.py
from rest_framework import viewsets
from drf_nested_views import viewsets as drf_nested_views

from .models import Domain, Nameserver
from .serializers import DomainSerializer, NameserverSerializer


class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()


class NameserverViewSet(drf_nested_views.ModelViewSet):
    """
    ModelViewSet from drf_nested_views use `serializer_class`
    attribute to extract the queryset (if yor serializer is 
    a ModelSerializer subclass). In this case, you don't need 
    provide it.
    """
    serializer_class = NameserverSerializer
```

Nested viewsets will use the `parent_lookup_kwargs` attribute from `NestedHyperlinkedModelSerializer` to perform all nested actions (list, retrieve, create, update, delete). If you not use a serilizer of this type in yor view, you must provide the attribute explicitly or override `get_parent_lookup_kwargs()` method:

```python
class NameserverViewSet(drf_nested_views.ReadOnlyModelViewSet):
    serializer_class = NameserverSerializer # is not a NestedHyperlinkedModelSerializer subclass
    parent_lookup_kwargs = {
        'domain_pk': 'domain__pk',
    }

    ## OR ##

    def get_parent_lookup_kwargs(self):
        return {
            'domain_pk': 'domain__pk',
        }
```

## Advanced Usage
### Customize viewsets
To create a base viewset class with only certain operations, inherit from `GenericViewSet` from `drf_nested_views.viewsets`, and mixin the required actions from `drf_nested_views.mixins`:

```python
from drf_nested_views.viewsets import GenericViewSet
from drf_nested_views import mixins as drf_nested_mixins

class CreateRetrieveDestroyViewSet(drf_nested_mixins.CreateModelMixin,
                                   drf_nested_mixins.RetrieveModelMixin,
                                   drf_nested_mixins.DestroyModelMixin,
                                   GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `destroy` actions.

    To use it, override the class and set the `serializer_class` attribute.
    """
    pass
```

### `GenericAPIView`
The entire base logic of this library is inside the class `GenericAPIView` from `drf_nested_views.generics`. If you need another behaviour or logic to your views you can construct a base class, inherit from it.

```python
from drf_nested_views.generics import GenericAPIView


class CustomAPIView(GenericAPIView):
    """
    A base class to improve another behaviour for
    nested resources
    """
    <statatement-1>
    .
    .
    .
    <statement-N>
```

`GenericAPIView` inherit from `GenericAPIView` of `rest_framework.generics` and overrides the methods `get_queryset()` and `filter_queryset()`. Besides override theese methods, another methods was added:

* **`get_parent_lookup_kwargs`** - Returns the parent lookup kwargs, a dictionary that maps URL kwargs into object lookup properties.
* **`get_parent_lookup`** - Returns the entire filter lookup for parent based on `parent_lookup_kwargs` and URL keyword arguments.


## Notes
* This library use the same name of [Django REST Framework](http://www.django-rest-framework.org/) for viewsets, generics and mixins classes. Keep this in mind when using both libraries within the same file and define aliases for imported modules.

## Release Notes
* 1.0.0 - 22/01/2018 - First release