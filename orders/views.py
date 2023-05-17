from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Order, OrderItem
from cart.utils.cart import Cart
from shop.models import Product

@login_required
def create_order(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user,status=True)
    for item in cart:
        n = int(item['price']) * int(item['quantity'])
        OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity'],totalprice=n
    )
    for n in Product.objects.all():
        product = get_object_or_404(Product, id=n.id)
        cart.remove(product)
    return redirect('orders:checkout', order_id=order.id)


@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'title':'Checkout' ,'order':order,'id':order_id}
    return render(request, 'checkout.html', context)


@login_required
def fake_payment(request, order_id):
    if request.method == 'POST':
        OrderItem.objects.filter(id=order_id).update(status='Pending delivery', payment=False)
        return redirect('orders:user_orders')
    return render(request,'payments.html')

@login_required
def CancelOrder(request, order_id,Orderitem_id):
    staus = set()
    OrderItem.objects.filter(id=Orderitem_id).update(status='Order cancelled', payment=False)
    for k in Order.objects.filter(id=order_id).all():
        for n in OrderItem.objects.filter(order=k.id):
            staus.add(n.status)
    if len(staus)==1:
        for value in staus:
            if value == 'Order cancelled':
              Order.objects.filter(id=order_id).update(status=False)

    return redirect('/orders/list')

@login_required
def user_orders(request):
    orders = request.user.orders.all()
    payment = OrderItem.objects.all()
    context = {'title':'Orders', 'orders': orders,'payment':payment}
    return render(request, 'user_orders.html', context)