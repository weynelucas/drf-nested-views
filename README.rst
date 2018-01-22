drf-nested-views
================

A set of views to work with `drf-nested-routers`_.

View the `full documentation on GitHub`_.

Instalation
-----------

You can install this library using pip:

::

    pip install drf-nested-views

Requirements
------------

This library was tested with the follow dependencies:

-  `Django`_ - 1.11
-  `Django REST Framework`_ - 3.7
-  `drf-nested-routers`_ - 0.90.0

Quickstart
----------

Configure your desired URL signatures:

.. code:: python

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

Configure serialization, with ``NestedHyperlinkedModelSerializer`` for
nested objects:

.. code:: python

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

Create your viewsets extending ``ModelViewSet`` or
``ReadOnlyModelViewSet`` from ``drf_nested_views.viewsets`` to improve
nested resources behaviour:

.. code:: python

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

.. _drf-nested-routers: https://github.com/alanjds/drf-nested-routers
.. _full documentation on GitHub: https://github.com/weynelucas/drf-nested-views/
.. _Django: https://www.djangoproject.com/
.. _Django REST Framework: http://www.django-rest-framework.org/