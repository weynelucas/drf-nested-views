from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        ordering = ['name']


class MailDrop(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']


class MailRecipient(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    maildrop = models.ForeignKey('MailDrop', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']