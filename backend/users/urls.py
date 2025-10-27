from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register-user"),
    path("<str:phone_number>/", views.UserProfileView.as_view(), name="user-profile"),
    path("<str:phone_number>/referrals/", views.UserReferralsView.as_view(), name="user-referrals"),
    path("<str:phone_number>/commissions/", views.UserCommissionSummaryView.as_view(), name="user-commissions"),
]
