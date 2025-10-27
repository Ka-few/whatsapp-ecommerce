from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Referral, ReferralCommission
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    ReferralSerializer,
    ReferralCommissionSerializer,
)
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import random
import string

class RegisterUserView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        name = request.data.get("name", "")

        if not phone_number:
            return Response(
                {"error": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(phone_number=phone_number)

        if created:
            # Generate unique referral code
            user.referral_code = self.generate_referral_code()
            user.name = name
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def generate_referral_code(self, length=8):
        """Generate a unique alphanumeric referral code"""
        while True:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not User.objects.filter(referral_code=code).exists():
                return code

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "phone_number"

class UserReferralsView(APIView):
    def get(self, request, phone_number):
        user = get_object_or_404(User, phone_number=phone_number)
        referrals = Referral.objects.filter(referrer=user)
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data)

class UserCommissionSummaryView(APIView):
    def get(self, request, phone_number):
        user = get_object_or_404(User, phone_number=phone_number)
        total_commission = (
            ReferralCommission.objects.filter(referrer=user)
            .aggregate(Sum("amount"))["amount__sum"] or 0
        )
        commissions = ReferralCommission.objects.filter(referrer=user)
        serializer = ReferralCommissionSerializer(commissions, many=True)
        return Response({
            "user": user.name,
            "total_commission": total_commission,
            "commissions": serializer.data
        })
