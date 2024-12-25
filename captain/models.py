from django.db import models
from accounts.models import Captain  # استيراد الكابتن الأساسي

class CaptainProfile(models.Model):
    captain_user = models.OneToOneField(
        Captain, 
        on_delete=models.CASCADE, 
        related_name="profile"  # اسم العلاقة للوصول بسهولة
    )
    license_number = models.CharField(max_length=100, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/captains/", blank=True, null=True)

    def __str__(self):
        return f"Profile for Captain: {self.captain_user.email}"
