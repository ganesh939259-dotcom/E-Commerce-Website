from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order,Category,Review
from django.db.models import Q
from django.core.mail import send_mail

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

    print("CHECKOUT CALLED")

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    print("BEFORE EMAIL")

    send_mail(
        'Order Confirmation',
        'your order is successfully delievered',
        'ganesh939259@gmail.com',
        ['nangiliganesh210@gmail.com'],
        fail_silently=False,
    )

    print("AFTER EMAIL")

    cart_items.delete()

    return render(request, 'success.html')
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('store:home')

import razorpay
from django.conf import settings
from django.shortcuts import render

@login_required
def payment(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    amount = int(total * 100)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(
        request,
        "payment.html",
        {
            "payment": payment,
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID
        }
    )
@login_required
def add_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        existing_review = Review.objects.filter(
            product=product,
            user=request.user
        ).first()

        if not existing_review:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

    return redirect(
        'store:product_detail',
        product_id=product.id
    )
def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = Review.objects.filter(
        product=product
    )

    return render(
        request,
        'product_details.html',
        {
            'product': product,
            'reviews': reviews
        }
    )