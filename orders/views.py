from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Product
from .carts import Cart
from .forms import CartAddForm
from .models import Order, OrderItem


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order})


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for i in cart:
            OrderItem.objects.create(
                order=order,
                product=i['product'],
                price=i['price'],
                quantity=i['quantity']
            )
        cart.clear()
        return redirect('orders:order_detail', order.id)
