from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import UserCheckoutForm,UserFormx

# Create your views here.

def CustomerHome(request):
    items =Item.objects.all()
    return render(request, "customer/index.html", {"items " : items})

def CustomerAbout(request):
    return render(request, "customer/about.html")
def CustomerMenu(request):
    items =Item.objects.all()
    data = {"title":"MENU","items":items}
    return render(request, "customer/menu.html", data)

def MenuDetail(request, id):
    items = Item.objects.get(pk=id)
    data = {"title":"detail","items":items}
    return render(request, "customer/detail.html", data)



# cart
def CustomerCart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    subtotal_list = []
    
    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        subtotal_list.append(subtotal)
        
    cart_items_subtotals = zip(cart_items, subtotal_list)
    
    data = {'cart_items_subtotals': cart_items_subtotals, 'total': total,"title":"Cart"}
    return render(request, "customer/cart.html", data)

@login_required
def cart_add(request, id):
    product = get_object_or_404(Item, pk=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('/menu/')

def item_clear(request, id):
    cart_item = get_object_or_404(Cart, pk=id)
    cart_item.delete()
    return redirect('/cart/')

def item_increment(request, id):
    cart_item = get_object_or_404(Cart, pk=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('/cart/')

def item_decrement(request, id):
    cart_item = get_object_or_404(Cart, pk=id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/cart/')

def cart_clear(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.delete()
    return redirect('/cart/')


def CheckOut(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    deliveryfee = 500
    total = subtotal + deliveryfee
    form = UserCheckoutForm()
    formx = UserFormx()
    if request.method == 'POST':
        form = UserCheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.user = request.user
            checkout.totalcash = total
            checkout.save()
            messages.success(request, "Order placed successfully!")
            cart_items.delete()
            return redirect('/order/', order_id=checkout.pk) # Redirect to the order detail page
        else:
                form = UserCheckoutForm()
                formx = UserFormx()
    
    data = {'formx': formx, 'form': form, 'total': total, 'title': 'CheckOut', 'subtotal': subtotal}
    return render(request, 'customer/checkout.html', data)


def Order(request, order_id):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    deliveryfee = 500
    total = subtotal + deliveryfee


    order = Order.objects.get(id=order_id)
    subtotal = sum(item.product.price * item.quantity for item in order.items.all())
    total = subtotal + deliveryfee

    if request.method == "POST":
        form = UserCheckoutForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return HttpResponse("Order details updated successfully!")
    else:
        form = UserCheckoutForm(instance=order)
        
    return render(request, 'customer/order.html', {'order': order, 'subtotal': subtotal, 'total': total, 'form': form})
