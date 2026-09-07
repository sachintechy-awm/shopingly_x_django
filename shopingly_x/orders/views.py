from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from accounts.models import Address


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:product_list')

    addresses = request.user.addresses.all()

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method', 'cod')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        order = Order.objects.create(user=request.user, address=address, payment_method=payment_method)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                price=item['price'],
                quantity=item['quantity'],
            )

        if payment_method == 'cod':
            order.status = 'pending'
            order.save()
            cart.clear()
            return redirect('orders:confirmation', order_id=order.id)
        else:
            return redirect('orders:payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart, 'addresses': addresses})


@login_required
def payment(request, order_id):
    """A mock payment page simulating a card/UPI gateway (no real transactions)."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.status = 'paid'
        order.save()
        cart = Cart(request)
        cart.clear()
        return redirect('orders:confirmation', order_id=order.id)
    return render(request, 'orders/payment.html', {'order': order})


@login_required
def confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
