# whatsapp_bot_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),

    # other apps will go here soon:
    # path('api/products/', include('products.urls')),
]
