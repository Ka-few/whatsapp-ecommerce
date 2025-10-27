from rest_framework import serializers
from .models import User, Referral, ReferralCommission

class UserSerializer(serializers.ModelSerializer):
    referred_by = serializers.StringRelatedField(read_only=True)
    total_referrals = serializers.IntegerField(read_only=True)
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "name",
            "referral_code",
            "referred_by",
            "total_referrals",
            "total_commission",
            "created_at",
        ]

class ReferralSerializer(serializers.ModelSerializer):
    referrer = serializers.StringRelatedField()
    referred = serializers.StringRelatedField()

    class Meta:
        model = Referral
        fields = ["id", "referrer", "referred", "created_at"]

class ReferralCommissionSerializer(serializers.ModelSerializer):
    referrer = serializers.StringRelatedField()
    order_id = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = ReferralCommission
        fields = ["id", "referrer", "order_id", "amount", "created_at"]
