from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import *


default_fields = ('id', 'url', 'name', 'created_at', 'updated_at')


class ClientSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = default_fields
        extra_kwargs = {
            'url': {'view_name': 'client-detail', 'lookup_field': 'pk'},
        }


class MailDropSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'client_pk': 'client_id'
    }

    class Meta:
        model = MailDrop
        fields = default_fields
        extra_kwargs = {
            'url': {'view_name': 'maildrop-detail', 'lookup_field': 'pk'},
        }


class MailRecipientSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'maildrop_pk': 'maildrop_id',
        'client_pk': 'maildrop__client_id',
    }

    class Meta:
        model = MailRecipient
        fields = default_fields
        extra_kwargs = {
            'url': {'view_name': 'recipient-detail', 'lookup_field': 'pk'},
        }