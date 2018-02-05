import json

from django.utils import timezone
from django.test import TestCase

from ... import models
from drf_nested_views.utils import to_related_lookup


class UtilsTestCase(TestCase):
    def setUp(self):
        client_id = 1,
        client_created_at = 1
        client_updated_at = 2
        mail_drop_id = 2
        maildrop_created_at = 3
        maildrop_updated_at = 4
        recipient_id = 3
        recipient_created_at = 5
        recipient_updated_at = 6

        # MailRecipient
        recipient = {
            'model': models.MailRecipient,
            'lookup': {
                'id': recipient_id,
                'created_at': recipient_created_at,
                'updated_at': recipient_updated_at,
                'maildrop_id': mail_drop_id,
                'maildrop__created_at': maildrop_created_at,
                'maildrop__updated_at': maildrop_updated_at,
                'maildrop__client_id': client_id,
                'maildrop__client__created_at': client_created_at,
                'maildrop__client__updated_at': client_updated_at,
            },
            'expected': {
                'id': mail_drop_id,
                'created_at': maildrop_created_at,
                'updated_at': maildrop_updated_at,
                'client_id': client_id,
                'client__created_at': client_created_at,
                'client__updated_at': client_updated_at,
            },
        }

        # MailDrop
        maildrop = {
            'model': models.MailDrop,
            'lookup': recipient['expected'],
            'expected': {
                'id': client_id,
                'created_at': client_created_at,
                'updated_at': client_updated_at,
            },
        }

        self.lookups = [
            recipient,
            maildrop,
        ]

    def test_to_related_lookup(self):
        for data in self.lookups:
            result = to_related_lookup(data['model'], data['lookup'])

            self.assertEqual(
                data['expected'].items(),
                result.items(),
            )