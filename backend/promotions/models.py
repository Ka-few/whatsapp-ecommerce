from django.db import models
from django.utils import timezone
from products.models import Product

class Promotion(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_products = models.ManyToManyField(Product, blank=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_type}: {self.discount_value})"

    def is_valid(self):
        """Check if the promotion is active and within date range."""
        now = timezone.now()
        return self.is_active and (self.start_date <= now <= (self.end_date or now))
