# 🛍️ WhatsApp Commerce API
## Author
## Francis Njoroge

A Django + Twilio-powered e-commerce backend that allows users to discover, order, and interact with products directly through **WhatsApp**.  
The system supports automated WhatsApp responses, product management, promotions, and analytics for seamless customer engagement.

---

## 🚀 Features

### 💬 WhatsApp Integration
- Connects via **Twilio WhatsApp API**.
- Automatically replies to user messages.
- Handles product inquiries, promotions, and order status.

### 🛒 E-commerce Backend
- Manage **Products**, **Orders**, and **Promotions**.
- RESTful API built with **Django REST Framework (DRF)**.
- Integrated **PostgreSQL** database for scalability.

### 📊 Analytics & Admin
- Admin dashboard via Django Admin.
- `/api/analytics/` endpoint for business insights.

### 🌐 Deployment Ready
- Fully containerized and deployable on **Render** or **Heroku**.
- Uses **Gunicorn** + **Whitenoise** for production-grade performance.
- CORS and environment variables configured for frontend integration.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Django 5 + Django REST Framework |
| **Database** | PostgreSQL |
| **Messaging** | Twilio WhatsApp API |
| **Server** | Gunicorn + Whitenoise |
| **Task Queue** | Celery + Redis *(optional)* |
| **Deployment** | Render |
| **Language** | Python 3.13 |

---

## 🛠️ Local Setup
## 1. Clone the repo
- git clone https://github.com/<your-username>/whatsapp-commerce.git
- cd whatsapp-commerce/backend
## 2. Create a virtual environment
- python -m venv venv
- source venv/bin/activate
## 3. Install dependencies
- pip install -r requirements.txt
## 4. Apply migrations
- python manage.py migrate
## 5. Run the server
- python manage.py runserver
## 6. Expose the webhook (for Twilio testing)
- ngrok http 8000
## 7. Set the webhook URL in Twilio
- https://<ngrok-url>/api/whatsapp/webhook/



