from django.db import models
from accounts.models import Captain, Client

class Profile(models.Model):
    captain = models.OneToOneField(
        Captain,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profile_app_captain_profile"  # تخصيص اسم فريد للعلاقة العكسية
    )
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profile_app_client_profile"  # تخصيص اسم فريد للعلاقة العكسية
    )
    country_code = models.CharField(max_length=5, default='+20')  # كود الدولة

    def __str__(self):
        if self.captain:
            return f"Captain Profile: {self.captain.email}"
        elif self.client:
            return f"Client Profile: {self.client.email}"
        return "Unassigned Profile"
