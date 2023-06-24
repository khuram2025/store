from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class MyAccountManager(BaseUserManager):
    def create_user(self, mobile_number, password=None):
        if not mobile_number:
            raise ValueError('Users must have a mobile number')

        user = self.model(
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password):
        user = self.create_user(
            mobile_number=mobile_number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=14, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='user_cover/', null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.mobile_number
