from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Referral system
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals'
    )
    total_referrals = models.PositiveIntegerField(default=0)
    total_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Auth/permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]  # email will be required when creating a superuser

    objects = UserManager()

    def __str__(self):
        return f"{self.name or self.phone_number}"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_random_string(length=8).upper()
        super().save(*args, **kwargs)
        
class Referral(models.Model):
    referrer = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='referrer_links'
    )
    referred = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='referred_links'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('referrer', 'referred')

    def __str__(self):
        return f"{self.referrer.phone_number} → {self.referred.phone_number}"


# --------------------------
# REFERRAL COMMISSION MODEL
# --------------------------
class ReferralCommission(models.Model):
    referrer = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='commissions'
    )
    order = models.ForeignKey(
        'orders.Order', on_delete=models.CASCADE, related_name='referral_commissions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission: {self.referrer.phone_number} - {self.amount}"