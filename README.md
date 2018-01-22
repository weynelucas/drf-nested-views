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

Nested viewsets will use the `parent_lookup_kwargs` attribute from `NestedHyperlinkedModelSerializer` to perform all nested actions (list, retrieve, create, update, delete). If you not use a serilizer of this type in yor view, you must provide the attribute explicitly or override `get_parent_lookup_kwargs()` method.

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
