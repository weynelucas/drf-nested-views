from rest_framework import viewsets
from drf_nested_views import viewsets as drf_nested_viewsets


from . import serializers, models


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()


class MailDropViewSet(drf_nested_viewsets.ModelViewSet):
    serializer_class = serializers.MailDropSerializer


class MailRecipientViewSet(drf_nested_viewsets.ModelViewSet):
    serializer_class = serializers.MailRecipientSerializer