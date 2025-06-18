import stripe
from django.conf import settings
from orders.models import Order
import logging

logger = logging.getLogger(__name__)

def initialize_stripe():
    stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_payment_intent(order):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.total * 100),  # Convert to cents
            currency='usd',
            metadata={
                'order_number': order.order_number,
                'user_id': order.user.id
            }
        )
        return payment_intent.client_secret
    except Exception as e:
        logger.error(f"Stripe payment creation failed: {str(e)}")
        raise