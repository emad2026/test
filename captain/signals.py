from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CaptainProfile
from accounts.models import Captain

@receiver(post_save, sender=Captain)
def create_or_update_captain_profile(sender, instance, created, **kwargs):
    """
    - إذا كان المستخدم جديدًا (created=True)، يتم إنشاء الملف الشخصي تلقائيًا.
    - إذا كان الملف الشخصي موجودًا، يتم تحديثه عند حفظ المستخدم.
    """
    if created:
        CaptainProfile.objects.create(captain_user=instance)
    else:
        # إذا كان الملف الشخصي موجودًا بالفعل، يتم حفظ التحديثات
        instance.profile.save()
