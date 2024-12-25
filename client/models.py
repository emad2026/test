from django.db import models
from accounts.models import Client  # استيراد العميل الأساسي

class ClientProfile(models.Model):
    client_user = models.OneToOneField(
        Client, 
        on_delete=models.CASCADE, 
        related_name="profile"  # اسم العلاقة للوصول بسهولة
    )
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/clients/", blank=True, null=True)

    def __str__(self):
        return f"Profile for Client: {self.client_user.email}"
