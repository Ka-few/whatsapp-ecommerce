from decimal import Decimal
from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from promotions.models import Promotion


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    promotion_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'items', 'promotion_code', 'created_at']
        read_only_fields = ['total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        promo_code = validated_data.pop('promotion_code', None)
        user = validated_data['user']

        # Lookup promotion
        promotion = None
        if promo_code:
            try:
                promo = Promotion.objects.get(code=promo_code, is_active=True)
                if promo.is_valid():
                    promotion = promo
                else:
                    raise serializers.ValidationError({
                        "promotion_code": "Invalid or inactive promotion code."
                    })
            except Promotion.DoesNotExist:
                raise serializers.ValidationError({
                    "promotion_code": "Invalid or inactive promotion code."
                })

        # ✅ Calculate total before creating Order
        total = Decimal(0)
        for item_data in items_data:
            product = item_data['product']  # Already a Product instance
            quantity = item_data['quantity']
            total += Decimal(product.price) * quantity

        if promotion:
            if promotion.discount_type == 'percentage':
                discount = (promotion.discount_value / Decimal(100)) * total
            elif promotion.discount_type == 'fixed':
                discount = promotion.discount_value
            else:
                discount = Decimal(0)
            total -= discount

        total = max(total, Decimal(0))

        # ✅ Now create Order with total_amount
        order = Order.objects.create(
            user=user,
            total_amount=total,
            promotion=promotion,
            status=validated_data.get('status', 'pending')
        )

        # Create OrderItems
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['product'].price
            )

        return order