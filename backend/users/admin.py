from django.contrib import admin
from .models import User, Referral, ReferralCommission


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "name", "referral_code", "referred_by", "total_referrals", "total_commission")
    search_fields = ("phone_number", "name", "referral_code")


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("referrer", "referred", "created_at")
    search_fields = ("referrer__phone_number", "referred__phone_number")


@admin.register(ReferralCommission)
class ReferralCommissionAdmin(admin.ModelAdmin):
    list_display = ("referrer", "order", "amount", "created_at")
