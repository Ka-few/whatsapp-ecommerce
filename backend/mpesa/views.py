from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mpesa_callback(request):
    """
    Placeholder view to handle M-Pesa callback.
    """
    # In a real implementation, you would process the callback data from Safaricom here
    print("Received M-Pesa callback")
    return JsonResponse({"status": "callback received"})