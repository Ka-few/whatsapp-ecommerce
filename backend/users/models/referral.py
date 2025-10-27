from django.db import models
from django.utils import timezone


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
