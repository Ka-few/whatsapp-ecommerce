from django.db import models
from django.utils.crypto import get_random_string


class User(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals'
    )
    total_referrals = models.PositiveIntegerField(default=0)
    total_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name or 'User'} - {self.phone_number}"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_random_string(length=8).upper()
        super().save(*args, **kwargs)
