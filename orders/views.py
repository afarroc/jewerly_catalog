from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm
import logging
import stripe

logger = logging.getLogger(__name__)

# Constants
DEFAULT_SHIPPING_COST = Decimal('5.00')
TAX_RATE = Decimal('0.08')  # 8%
stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
@login_required
def checkout(request):
    """Handle the checkout process and order creation."""
    logger.info(f"Checkout process initiated for user {request.user.id}")
    
    try:
        cart = Cart.objects.get(user=request.user)
        logger.info(f"Cart found with {cart.total_items} items (ID: {cart.id})")
    except Cart.DoesNotExist:
        logger.warning(f"No cart found for user {request.user.id}")
        messages.error(request, "Your shopping cart was not found")
        return redirect('home:index')

    if cart.total_items == 0:
        logger.warning("Empty cart detected during checkout")
        messages.warning(request, "Your cart is empty")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        
        if form.is_valid():
            if not request.POST.get('agree_terms'):
                messages.error(request, "You must accept the terms and conditions")
                return redirect('orders:checkout')
                
            try:
                with transaction.atomic():
                    # Create and validate order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.subtotal = cart.subtotal
                    order.shipping_cost = DEFAULT_SHIPPING_COST
                    order.tax = (cart.subtotal * TAX_RATE).quantize(Decimal('0.01'))
                    order.total = (order.subtotal + order.shipping_cost + order.tax).quantize(Decimal('0.01'))
                    
                    # Validate payment method
                    payment_method = form.cleaned_data.get('payment_method')
                    if payment_method not in dict(Order.PAYMENT_CHOICES).keys():
                        raise ValueError("Invalid payment method selected")
                    
                    order.save()
                    
                    # Create order items
                    for cart_item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price
                        )

                    # Process payment based on selected method
                    if payment_method == 'credit_card':
                        try:
                            intent = stripe.PaymentIntent.create(
                                amount=int(order.total * 100),
                                currency='usd',
                                metadata={
                                    'order_id': order.id,
                                    'user_id': request.user.id,
                                    'payment_method': payment_method
                                },
                                description=f"Order #{order.order_number}"
                            )
                            
                            if settings.DEBUG:
                                stripe.PaymentIntent.confirm(
                                    intent.id,
                                    payment_method='pm_card_visa'
                                )
                            
                            order.payment_status = True
                            order.payment_date = timezone.now()
                            order.save()
                            
                        except stripe.error.StripeError as e:
                            logger.error(f"Stripe payment failed: {str(e)}")
                            messages.error(request, f"Payment processing failed: {e.user_message}")
                            return redirect('orders:checkout')
                            
                    elif payment_method == 'paypal':
                        # PayPal processing would go here
                        order.payment_status = True
                        order.payment_date = timezone.now()
                        order.save()
                    
                    # Clear cart and send confirmation
                    cart.clear()
                    send_order_confirmation(order)
                    
                    messages.success(request, "Your order has been placed successfully!")
                    return redirect('orders:order_confirmation', order_id=order.id)

            except Exception as e:
                logger.error(f"Checkout failed: {str(e)}", exc_info=True)
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('orders:checkout')
                
        else:
            logger.warning(f"Form validation failed: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'title': 'Checkout',
        'cart': cart,
        'form': form,
        'tax': (cart.subtotal * TAX_RATE).quantize(Decimal('0.01')),
        'shipping_cost': DEFAULT_SHIPPING_COST,
        'total': (cart.subtotal + DEFAULT_SHIPPING_COST + (cart.subtotal * TAX_RATE)).quantize(Decimal('0.01')),
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    
    return render(request, 'orders/checkout.html', context)

@csrf_exempt
@login_required
def create_order_ajax(request):
    """AJAX endpoint for order creation."""
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            form = CheckoutForm(request.POST, user=request.user)
            
            if form.is_valid():
                with transaction.atomic():
                    # Create order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.subtotal = cart.subtotal
                    order.shipping_cost = DEFAULT_SHIPPING_COST
                    order.tax = (cart.subtotal * TAX_RATE).quantize(Decimal('0.01'))
                    order.total = (order.subtotal + order.shipping_cost + order.tax).quantize(Decimal('0.01'))
                    order.save()

                    # Create order items
                    for cart_item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price
                        )

                    # Create Stripe PaymentIntent
                    intent = stripe.PaymentIntent.create(
                        amount=int(order.total * 100),  # Amount in cents
                        currency='usd',
                        metadata={
                            'order_id': order.id,
                            'user_id': request.user.id
                        },
                        description=f"Order #{order.order_number}"
                    )

                    return JsonResponse({
                        'success': True,
                        'order_id': order.id,
                        'client_secret': intent.client_secret
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.as_json()
                }, status=400)
                
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False}, status=405)

def process_order(request, cart, form):
    """Process and create a new order (legacy fallback)."""
    with transaction.atomic():
        # Create order
        order = form.save(commit=False)
        order.user = request.user
        order.subtotal = cart.subtotal
        order.shipping_cost = DEFAULT_SHIPPING_COST
        order.tax = (cart.subtotal * TAX_RATE).quantize(Decimal('0.01'))
        order.total = (order.subtotal + order.shipping_cost + order.tax).quantize(Decimal('0.01'))
        order.save()

        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Process payment
        if not process_payment(order):
            raise Exception("Payment processing failed")

        # Update order status
        order.payment_status = True
        order.payment_date = timezone.now()
        order.save()

        # Clear cart
        cart.clear()

        # Send confirmation
        send_order_confirmation(order)
        
        messages.success(request, "Your order has been placed successfully!")
        logger.info(f"Order {order.order_number} created successfully")
        return redirect('orders:order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    """Display order confirmation page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'title': f'Order Confirmation #{order.order_number}',
        'order': order,
    }
    return render(request, 'orders/confirmation.html', context)

@login_required
def order_history(request):
    """Display paginated order history for the user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Order History',
        'page_obj': page_obj,
    }
    return render(request, 'orders/history.html', context)

@login_required
def order_detail(request, order_id):
    """Display detailed order information."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'title': f'Order Details #{order.order_number}',
        'order': order,
    }
    return render(request, 'orders/detail.html', context)

@login_required
def order_invoice(request, order_id):
    """Generate order invoice."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'title': f'Invoice #{order.order_number}',
        'order': order,
    }
    return render(request, 'orders/invoice.html', context)

@login_required
def cancel_order(request, order_id):
    """Handle order cancellation request."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status not in ['pending', 'processing']:
        messages.error(request, "This order cannot be cancelled at this stage")
        logger.warning(f"Cancel attempt for non-cancellable order {order.order_number}")
        return redirect('orders:order_detail', order_id=order.id)
    
    try:
        with transaction.atomic():
            # Create Stripe refund if payment was processed
            if order.payment_status:
                try:
                    payment_intents = stripe.PaymentIntent.list(
                        metadata={'order_id': order.id}
                    )
                    for intent in payment_intents.auto_paging_iter():
                        stripe.Refund.create(
                            payment_intent=intent.id,
                            reason='requested_by_customer'
                        )
                except stripe.error.StripeError as e:
                    logger.error(f"Stripe refund failed: {str(e)}")

            order.status = 'cancelled'
            order.save()
            send_order_cancellation(order)
            messages.success(request, "Order has been cancelled successfully")
            logger.info(f"Order {order.order_number} cancelled by user")
    except Exception as e:
        messages.error(request, "Failed to cancel order")
        logger.error(f"Order cancellation failed: {str(e)}")
    
    return redirect('orders:order_detail', order_id=order.id)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)

    # Handle payment success
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent.metadata.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = True
            order.payment_date = timezone.now()
            order.save()
            logger.info(f"Payment succeeded for order {order.order_number}")
        except Order.DoesNotExist:
            logger.error(f"Order {order_id} not found for payment intent {payment_intent.id}")

    return HttpResponse(status=200)

# Helper Functions
def process_payment(order):
    """Process payment through Stripe."""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.total * 100),
            currency='usd',
            metadata={
                'order_id': order.id,
                'user_id': order.user.id
            },
            description=f"Order #{order.order_number}"
        )
        logger.info(f"Payment processed for order {order.order_number}")
        return True
    except stripe.error.StripeError as e:
        logger.error(f"Payment failed for order {order.order_number}: {str(e)}")
        return False

def send_order_confirmation(order):
    """Send order confirmation email."""
    subject = f"Order Confirmation #{order.order_number}"
    context = {'order': order}
    
    text_message = render_to_string('orders/emails/order_confirmation.txt', context)
    html_message = render_to_string('orders/emails/order_confirmation.html', context)
    
    send_mail(
        subject,
        text_message,
        'orders@fantasyjewelry.com',
        [order.user.email],
        html_message=html_message
    )
    logger.info(f"Confirmation email sent for order {order.order_number}")

def send_order_cancellation(order):
    """Send order cancellation email."""
    subject = f"Order Cancelled #{order.order_number}"
    context = {'order': order}
    
    text_message = render_to_string('orders/emails/cancellation.txt', context)
    html_message = render_to_string('orders/emails/cancellation.html', context)
    
    send_mail(
        subject,
        text_message,
        'support@fantasyjewelry.com',
        [order.user.email],
        html_message=html_message
    )
    logger.info(f"Cancellation email sent for order {order.order_number}")
    
def terms_and_conditions(request):
    context = {
        'title': 'Terms and Conditions'
    }
    return render(request, 'orders/legal/terms.html', context)