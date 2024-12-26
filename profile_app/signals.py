from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Captain, Client
from .models import Profile

@receiver(post_save, sender=Captain)
def create_captain_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(captain=instance)

@receiver(post_save, sender=Client)
def create_client_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(client=instance)
