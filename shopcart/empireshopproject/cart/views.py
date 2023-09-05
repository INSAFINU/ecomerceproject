from django.shortcuts import render, get_object_or_404,redirect
from empireshopapp.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# def _cart_id(request):
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart
import uuid

def _cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())  # Generate a unique cart_id using UUID
        request.session['cart_id'] = cart_id
    return cart_id

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_id = _cart_id(request)
    cart_queryset = Cart.objects.filter(cart_id=cart_id)

    if cart_queryset.exists():
        cart = cart_queryset.first()
    else:
        cart = Cart.objects.create(cart_id=cart_id)
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except Cart.DoesNotExist:
        cart_items = None
    except CartItem.DoesNotExist:
        cart_items = None

    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
