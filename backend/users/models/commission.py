from django.db import models


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
