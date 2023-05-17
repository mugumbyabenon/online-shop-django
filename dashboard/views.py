from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from shop.models import Product
from accounts.models import User
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, EditProductForm





@user_passes_test(lambda u: u.is_admin)
def products(request):
    products = Product.objects.all()
    context = {'title':'Products' ,'products':products}
    return render(request, 'products.html', context)


@user_passes_test(lambda u: u.is_admin)
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added Successfuly!')
            return redirect('dashboard:add_product')
    else:
        form = AddProductForm()
    context = {'title':'Add Product', 'form':form}
    return render(request, 'add_product.html', context)


@user_passes_test(lambda u: u.is_admin)
def delete_product(request, id):
    product = Product.objects.filter(id=id).delete()
    messages.success(request, 'product has been deleted!', 'success')
    return redirect('dashboard:products')


@user_passes_test(lambda u: u.is_admin)
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated', 'success')
            return redirect('dashboard:products')
    else:
        form = EditProductForm(instance=product)
    context = {'title': 'Edit Product', 'form':form}
    return render(request, 'edit_product.html', context)


@user_passes_test(lambda u: u.is_admin)
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added Successfuly!')
            return redirect('dashboard:add_category')
    else:
        form = AddCategoryForm()
    context = {'title':'Add Category', 'form':form}
    return render(request, 'add_category.html', context)


@user_passes_test(lambda u: u.is_admin)
def orders(request):
    orders = OrderItem.objects.filter(status='Pending delivery').all()
    context = {'title':'Orders', 'orders':orders}
    return render(request, 'orders.html', context)

@user_passes_test(lambda u: u.is_admin)
def ConfirmOrders(request,id):
    OrderItem.objects.filter(id=id).update(status ='Delivered')
    return redirect('/dashboard/orders')


@user_passes_test(lambda u: u.is_admin)
def order_detail(request, id):
    order = Order.objects.filter(id=id).first()
    items = OrderItem.objects.filter(order=id).all()
    context = {'title':'order detail', 'items':items, 'order':order}
    return render(request, 'order_detail.html', context)