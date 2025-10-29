from django.db import models
from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class WhatsAppSession(models.Model):
    user_phone = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    current_step = models.CharField(max_length=20, default='start')
    selected_product_id = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user(self):
        return self.user or User.objects.filter(phone_number=self.user_phone).first()
    
class WhatsAppSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="whatsappsession")
    state = models.CharField(max_length=50, default="idle")
    last_message = models.TextField(blank=True, null=True)
    context = models.JSONField(default=dict, blank=True)  # For holding temporary data (e.g. selected product)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name or self.user.phone_number} - {self.state}"
