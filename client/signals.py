from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClientProfile
from accounts.models import Client

@receiver(post_save, sender=Client)
def create_or_update_client_profile(sender, instance, created, **kwargs):
    """
    - إذا كان المستخدم جديدًا (created=True)، يتم إنشاء الملف الشخصي تلقائيًا.
    - إذا كان الملف الشخصي موجودًا، يتم حفظ التحديثات عند حفظ المستخدم.
    """
    if created:
        ClientProfile.objects.create(client_user=instance)
    else:
        # إذا كان الملف الشخصي موجودًا بالفعل، يتم حفظ التحديثات
        instance.profile.save()
