import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from users.models import User
from .models import WhatsAppSession
from .utils import send_whatsapp_message

API_BASE_URL = "http://127.0.0.1:8000/api"


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        try:
            data = request.POST.dict()
            print("📩 Incoming WhatsApp data:", data)

            incoming_msg = data.get("Body", "").strip().lower()
            from_number = data.get("From", "")
            user_phone = from_number.replace("whatsapp:", "")

            # --- Get or create user ---
            user, _ = User.objects.get_or_create(phone_number=user_phone)

            # --- Get or create session ---
            session, _ = WhatsAppSession.objects.get_or_create(user=user)
            print(f"🧠 Current state: {session.state}")

            # === STATE MACHINE ===

            # STEP 1: WELCOME / MENU
            if incoming_msg in ["hi", "hello", "menu"]:
                session.state = "menu"
                session.context = {}
                session.save()
                send_menu(from_number)
                return JsonResponse({"status": "menu sent"})

            # STEP 2: MENU OPTIONS
            elif session.state == "menu":
                if incoming_msg == "1":  # Browse Products
                    session.state = "browsing_products"
                    session.save()
                    send_products(from_number)
                    return JsonResponse({"status": "products sent"})

                elif incoming_msg == "2":  # View Promotions
                    session.state = "browsing_promotions"
                    session.save()
                    send_promotions(from_number)
                    return JsonResponse({"status": "promotions sent"})

                elif incoming_msg == "3":  # My Orders
                    session.state = "checking_orders"
                    session.save()
                    send_orders(from_number, user_phone)
                    return JsonResponse({"status": "orders sent"})

                else:
                    send_whatsapp_message(from_number, "❓ Invalid option. Reply *menu* to start again.")
                    return JsonResponse({"status": "invalid menu"})

            # STEP 3: BROWSING PRODUCTS
            elif session.state == "browsing_products":
                if incoming_msg == "menu":
                    session.state = "menu"
                    session.save()
                    send_menu(from_number)
                    return JsonResponse({"status": "back to menu"})

                try:
                    # User selects a product by number (1, 2, 3)
                    product_index = int(incoming_msg) - 1
                    products = requests.get(f"{API_BASE_URL}/products/").json()
                    if 0 <= product_index < len(products):
                        product = products[product_index]
                        session.context["current_product"] = product
                        session.state = "awaiting_quantity"
                        session.save()
                        send_whatsapp_message(
                            from_number,
                            f"🛒 You selected *{product['name']}* (KES {product['price']}).\nHow many units would you like?",
                        )
                        return JsonResponse({"status": "product selected"})
                    else:
                        send_whatsapp_message(from_number, "⚠️ Invalid product number.")
                except ValueError:
                    send_whatsapp_message(from_number, "❓ Please enter a valid number.")
                return JsonResponse({"status": "awaiting quantity"})

            # STEP 4: QUANTITY INPUT
            elif session.state == "awaiting_quantity":
                if incoming_msg == "menu":
                    session.state = "menu"
                    session.context = {}
                    session.save()
                    send_menu(from_number)
                    return JsonResponse({"status": "back to menu"})

                if incoming_msg.isdigit():
                    quantity = int(incoming_msg)
                    product = session.context.get("current_product")

                    if not product:
                        send_whatsapp_message(from_number, "⚠️ No product selected. Please select a product first.")
                        session.state = "browsing_products"
                        session.save()
                        send_products(from_number)
                        return JsonResponse({"status": "no product selected"})

                    # Initialize cart if it doesn't exist
                    cart = session.context.get("cart", [])
                    cart.append({"product": product, "quantity": quantity})
                    session.context["cart"] = cart
                    session.state = "awaiting_more_items"
                    session.save()

                    send_whatsapp_message(
                        from_number,
                        f"✅ Added {quantity} x {product['name']} to your cart.\n"
                        "Do you want to add more items? Reply *yes* or *checkout*."
                    )
                    return JsonResponse({"status": "item added to cart"})
                else:
                    send_whatsapp_message(from_number, "⚠️ Please enter a valid number for quantity.")
                return JsonResponse({"status": "invalid quantity"})

            # STEP 4.5: AWAITING MORE ITEMS
            elif session.state == "awaiting_more_items":
                if incoming_msg == "yes":
                    session.state = "browsing_products"
                    session.save()
                    send_products(from_number)
                    return JsonResponse({"status": "browsing more products"})
                elif incoming_msg == "checkout":
                    session.state = "confirming_order"
                    session.save()
                    send_confirmation_message(from_number, session.context.get("cart", []))
                    return JsonResponse({"status": "proceeding to checkout"})
                elif incoming_msg == "menu":
                    session.state = "menu"
                    session.context = {}
                    session.save()
                    send_menu(from_number)
                    return JsonResponse({"status": "back to menu"})
                else:
                    send_whatsapp_message(from_number, "❓ Reply *yes* to add more items or *checkout* to confirm your order.")
                    return JsonResponse({"status": "invalid option for more items"})

            # STEP 5: CONFIRM ORDER
            elif session.state == "confirming_order":
                if incoming_msg == "yes":
                    cart = session.context.get("cart", [])
                    if not cart:
                        send_whatsapp_message(from_number, "⚠️ Your cart is empty. Please add some products first.")
                        session.state = "menu"
                        session.context = {}
                        session.save()
                        send_menu(from_number)
                        return JsonResponse({"status": "empty cart"})

                    order_items_payload = []
                    total_amount = 0
                    for item in cart:
                        product = item["product"]
                        quantity = item["quantity"]
                        order_items_payload.append({
                            "product": product["id"],
                            "quantity": quantity,
                            "price": product["price"]
                        })
                        total_amount += float(product["price"]) * quantity

                    # Create order in backend
                    order_payload = {
                        "user": user.id,
                        "items": order_items_payload,
                        "total_amount": total_amount,
                        "status": "pending",
                    }

                    resp = requests.post(f"{API_BASE_URL}/orders/", json=order_payload)
                    if resp.status_code in [200, 201]:
                        send_whatsapp_message(
                            from_number,
                            f"🎉 Order placed successfully!\nOrder total: *KES {total_amount:,.2f}*\nWe’ll notify you once it’s confirmed."
                        )
                    else:
                        send_whatsapp_message(from_number, "⚠️ Could not create order, please try again later.")

                    session.state = "menu"
                    session.context = {}
                    session.save()
                    send_menu(from_number)
                    return JsonResponse({"status": "order confirmed"})

                elif incoming_msg == "menu":
                    session.state = "menu"
                    session.context = {}
                    session.save()
                    send_menu(from_number)
                    return JsonResponse({"status": "back to menu"})

                else:
                    send_whatsapp_message(from_number, "❓ Reply *yes* to confirm or *menu* to cancel.")
                return JsonResponse({"status": "awaiting confirmation"})

            # Default fallback
            else:
                send_whatsapp_message(from_number, "🤖 I didn’t understand that. Reply *menu* to start.")
                return JsonResponse({"status": "fallback"})

        except Exception as e:
            print(f"❌ Webhook error: {e}")
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Webhook active"}, status=200)


# --- Helper functions ---
def send_menu(to):
    msg = (
        "👋 *Welcome to Mama Mboga!*\n\n"
        "1️⃣ View Products\n"
        "2️⃣ View Promotions\n"
        "3️⃣ My Orders"
    )
    send_whatsapp_message(to, msg)

def send_confirmation_message(to, cart):
    if not cart:
        send_whatsapp_message(to, "Your cart is empty.")
        return

    message_lines = ["✅ *Confirm your order:*\n"]
    total_amount = 0

    for item in cart:
        product = item["product"]
        quantity = item["quantity"]
        item_total = float(product["price"]) * quantity
        total_amount += item_total
        message_lines.append(f"{quantity} x {product['name']} (KES {product['price']}) = KES {item_total:,.2f}")

    message_lines.append(f"\n*Total: KES {total_amount:,.2f}*\n")
    message_lines.append("Reply *yes* to confirm or *menu* to cancel.")

    send_whatsapp_message(to, "\n".join(message_lines))

def send_products(to):
    resp = requests.get(f"{API_BASE_URL}/products/")
    if resp.status_code == 200:
        products = resp.json()
        if products:
            msg_lines = ["🛍 *Available Products:*"]
            for i, p in enumerate(products[:5], start=1):
                msg_lines.append(f"{i}. {p['name']} - KES {p['price']}")
            msg_lines.append("\nReply with the number to select a product or *menu* to cancel.")
            send_whatsapp_message(to, "\n".join(msg_lines))
        else:
            send_whatsapp_message(to, "No products available right now.")
    else:
        send_whatsapp_message(to, "⚠️ Could not load products.")


def send_promotions(to):
    resp = requests.get(f"{API_BASE_URL}/promotions/")
    if resp.status_code == 200:
        promos = resp.json()
        if promos:
            lines = ["🎉 *Promotions:*"]
            for promo in promos:
                lines.append(f"• {promo['code']} - {promo['description']}")
            lines.append("\nReply *menu* to go back.")
            send_whatsapp_message(to, "\n".join(lines))
        else:
            send_whatsapp_message(to, "No promotions available.")
    else:
        send_whatsapp_message(to, "⚠️ Could not load promotions.")


def send_orders(to, user_phone):
    resp = requests.get(f"{API_BASE_URL}/orders/?user={user_phone}")
    if resp.status_code == 200:
        orders = resp.json()
        if orders:
            lines = ["📦 *Your Orders:*"]
            for order in orders[:3]:
                lines.append(f"Order #{order['id']} - Total: KES {order['total_amount']}")
            lines.append("\nReply *menu* to go back.")
            send_whatsapp_message(to, "\n".join(lines))
        else:
            send_whatsapp_message(to, "You have no orders yet.")
    else:
        send_whatsapp_message(to, "⚠️ Could not fetch orders.")
