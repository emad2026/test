from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client, ClientProfile
from django.apps import apps


@receiver(post_save, sender=Client)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        ClientProfile.objects.get_or_create(client=instance)
