from cProfile import Profile
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from accounts.models import Client, Captain

class CaptainManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and returns a standard user.
        """
        if not email:
            raise ValueError(_("An email address is required"))

        if not first_name or not last_name:
            raise ValueError(_("First and last names are required"))

        #email = self.normalize_email(email)
        #username = email.split('@')[0]
        
        extra_fields.setdefault('is_active', True)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_captain_profile(sender, instance, created, **kwargs):
         if created:
            Profile.objects.create(captain=instance)  # استبدال user بـ captain
            post_save.connect(create_captain_profile, sender=Captain)  # type: ignore # تعديل الـ sender ليكون Captain


 
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password=password, **extra_fields)



class ClientManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and returns a standard user.
        """
        if not email:
            raise ValueError(_("An email address is required"))

        if not first_name or not last_name:
            raise ValueError(_("First and last names are required"))

        #email = self.normalize_email(email)
        #username = email.split('@')[0]
        
        extra_fields.setdefault('is_active', True)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_client_profile(sender, instance, created, **kwargs):
       if created:
        Profile.objects.create(client=instance)  # استبدال user بـ client
        post_save.connect(create_client_profile, sender=Client)  # type: ignore # تعديل الـ sender ليكون Client


    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password=password, **extra_fields)
