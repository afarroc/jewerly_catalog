from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import json

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Actualiza el estado de la orden
        order = Order.objects.get(id=payment_intent.metadata.order_id)
        order.payment_status = True
        order.save()

    return HttpResponse(status=200)