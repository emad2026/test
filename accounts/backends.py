'''
from django.contrib.auth.backends import BaseBackend
from .models import Captain, Client
from django.contrib.auth.hashers import check_password

class CaptainBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            captain = Captain.objects.get(email=email)
            if captain and check_password(password, captain.password):
                return captain
        except Captain.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Captain.objects.get(pk=user_id)
        except Captain.DoesNotExist:
            return None

class ClientBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            client = Client.objects.get(email=email)
            if client and check_password(password, client.password):
                return client
        except Client.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None
'''