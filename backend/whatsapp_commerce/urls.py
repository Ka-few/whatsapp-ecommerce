from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .views import AnalyticsView

# Root view for Render health check or basic status
def home(request):
    return JsonResponse({
        "message": "WhatsApp E-commerce API is live 🚀",
        "status": "running",
        "endpoints": {
            "users": "/api/users/",
            "products": "/api/products/",
            "orders": "/api/orders/",
            "promotions": "/api/promotions/",
            "whatsapp": "/api/whatsapp/",
            "analytics": "/api/analytics/"
        }
    })

urlpatterns = [
    path("", home, name="home"),  # 👈 new root route
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/products/", include("products.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/promotions/", include("promotions.urls")),
    path("api/whatsapp/", include("whatsapp.urls")),
    path("api/analytics/", AnalyticsView.as_view(), name="analytics"),
]

