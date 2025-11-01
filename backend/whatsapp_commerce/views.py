from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from orders.models import Order
from users.models import User
from django.db.models import Sum

class AnalyticsView(APIView):
    def get(self, request, format=None):
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_users = User.objects.count()
        total_revenue = Order.objects.aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0

        data = {
            'totalProducts': total_products,
            'totalOrders': total_orders,
            'totalUsers': total_users,
            'totalRevenue': total_revenue,
        }
        return Response(data)
