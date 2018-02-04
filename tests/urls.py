"""
Routes config

/clients/
/clients/{pk}/
/clients/{client_pk}/maildrops/
/clients/{client_pk}/maildrops/{maildrop_pk}/
/clients/{client_pk}/maildrops/{maildrop_pk}/recipients/
/clients/{client_pk}/maildrops/{maildrop_pk}/recipients/{pk}/
"""
from django.conf.urls import url, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views


router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, 'client')

# Client nested URLs
client_router = NestedDefaultRouter(router, r'clients', lookup='client')
client_router.register(r'maildrops', views.MailDropViewSet, base_name='maildrop')

# MailDrop nested URLs
maildrop_router = NestedDefaultRouter(router, r'maildrops', lookup='maildrop')
maildrop_router.register(r'recipients', views.MailRecipientViewSet, base_name='recipient') 


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(client_router.urls)),
    url(r'^', include(maildrop_router.urls)),
]