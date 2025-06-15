from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
from decimal import Decimal
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm
import logging

logger = logging.getLogger(__name__)

# Constants
DEFAULT_SHIPPING_COST = Decimal('5.00')
TAX_RATE = Decimal('0.08')  # 8%

@login_required
def checkout(request):
    """Handle the checkout process and order creation."""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your shopping cart was not found")
        return redirect('home:index')

    if cart.total_items == 0:
        messages.warning(request, "Your cart is empty")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        
        if form.is_valid():
            try:
                return process_order(request, cart, form)
            except Exception as e:
                logger.error(f"Checkout error: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while processing your order")
                return redirect('orders:checkout')
    else:
        form = CheckoutForm(user=request.user)
    
    # Calculate all amounts as Decimal
    shipping_cost = DEFAULT_SHIPPING_COST
    tax = (cart.subtotal * TAX_RATE).quantize(Decimal('0.01'))
    total = (cart.subtotal + shipping_cost + tax).quantize(Decimal('0.01'))

    context = {
        'title': 'Checkout',
        'cart': cart,
        'form': form,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'total': total
    }
    return render(request, 'orders/checkout.html', context)

def process_order(request, cart, form):
    """Process and create a new order."""
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

        # Process payment (simulated)
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
            order.status = 'cancelled'
            order.save()
            send_order_cancellation(order)
            messages.success(request, "Order has been cancelled successfully")
            logger.info(f"Order {order.order_number} cancelled by user")
    except Exception as e:
        messages.error(request, "Failed to cancel order")
        logger.error(f"Order cancellation failed: {str(e)}")
    
    return redirect('orders:order_detail', order_id=order.id)

# Helper Functions
def process_payment(order):
    """Simulate payment processing (replace with real payment gateway)."""
    logger.info(f"Processing payment for order {order.order_number}")
    return True  # In production, implement actual payment processing

def send_order_confirmation(order):
    """Send order confirmation email."""
    subject = f"Order Confirmation #{order.order_number}"
    context = {'order': order}
    
    text_message = render_to_string('orders/emails/confirmation.txt', context)
    html_message = render_to_string('orders/emails/confirmation.html', context)
    
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