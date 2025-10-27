# whatsapp_bot_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    # other apps will go here soon:
    # path('api/products/', include('products.urls')),
]
