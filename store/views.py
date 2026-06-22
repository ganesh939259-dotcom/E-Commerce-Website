from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order,Category
from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('store:home')


@login_required
def cart_view(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def increase_quantity(request, product_id):

    cart_item = get_object_or_404(
        Cart,
        user=request.user,
        product_id=product_id
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('store:cart')


@login_required
def decrease_quantity(request, product_id):

    cart_item = get_object_or_404(
        Cart,
        user=request.user,
        product_id=product_id
    )

    cart_item.quantity -= 1

    if cart_item.quantity > 0:
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('store:cart')


@login_required
def place_order(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if cart_items.exists():
        Order.objects.create(
            user=request.user,
            total_price=total
        )

        cart_items.delete()

    return redirect('store:order_history')


@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'order_history.html',
        {'orders': orders}
    )
@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    Order.objects.create(
        user=request.user,
        total_price=total
    )

    cart_items.delete()

    return render(request, 'success.html')
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('store:home')