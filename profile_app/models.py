from django.db import models
from accounts.models import  Client


class ClientProfile(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='client_profile')
    country_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.client.first_name} {self.client.last_name}"
