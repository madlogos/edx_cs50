from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import logging
import datetime
from .models import Category, Product, Topping, Addition, Item, Cart, Order, \
    ItemTopping, ItemAddition, CartItem, OrderItem
from .udf import *


# Create your views here.
@login_required
def index(request):
    if request.method == "POST":
        return HttpResponse({'message': ['success', 'Cart item added.']})
    else:
        products = Product.objects.all()
        return render(request, "orders/index.html", {"products": products})

@login_required
def pick_product(request, id):
    if request.method == "POST":
        qty = to_num(request.POST['qty'])
        if qty is None or qty == 0:
            return HttpResponse("<script>window.close();</script>")

        toppings = clean_form_data(request.POST)
        n_topping = Product.objects.get(id=id).n_topping
        if sum(toppings.values()) != n_topping:
            return HttpResponse("<script>alert('This product should have " + str(n_topping) + " topping\(s\).')</script>")
        additions = clean_form_data(request.POST, {'ptn': r'addition_(\d+)$', 'rpl': r'\1'})

        # prepare cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        product = Product.objects.get(pk=id)
        item = Item(product=product, quantity=qty, price=product.price)
        
        # judge if duplicated
        itm_dup = False
        itm_trk = {'product': item.product.id, 'price': item.price, 'topping': dict(), 'addition': dict()}
        if len(toppings) > 0:
            for key in toppings:
                topping = Topping.objects.get(id=to_num(key))
                itm_trk['topping'][key] = toppings[key]
                itm_trk['price'] += topping.price * toppings[key]
        if len(additions) > 0:
            for key in additions:
                addition = Addition.objects.get(id=to_num(key))
                itm_trk['addition'][key] = additions[key]
                itm_trk['price'] += addition.price * additions[key]

        ## if duplicate, add 1
        for itm in cart.cartitem_set.all():
            itm_str = show_item(itm.item)
            if itm_trk == itm_str:
                itm_dup = True
                itm.quantity += qty
                itm.save()
                break
        
        ## if not duplicate, insert record
        if not itm_dup:
            item.save()
            if len(toppings) > 0:
                for key in toppings:
                    topping = Topping.objects.get(id=to_num(key))
                    ItemTopping.objects.create(item=item, topping=topping, quantity=toppings[key])
                    item.price += topping.price * toppings[key]
            if len(additions) > 0:
                for key in additions:
                    addition = Addition.objects.get(id=to_num(key))
                    ItemAddition.objects.create(item=item, addition=addition, quantity=additions[key])
                    item.price += addition.price * additions[key]
            item.save()
            CartItem.objects.create(cart=cart, item=item, quantity=qty)

        return redirect(reverse('cart'))
    else:
        products = Product.objects.get(id=id)
        toppings = Topping.objects.all()
        additions = Addition.objects.filter(size=products.size)
        return render(request, "orders/pick_product.html",
            {"product": products, "toppings": toppings, "additions": additions})

@login_required
def cart(request):
    if request.method == "POST":
        # save the form
        cart = Cart.objects.get(user=request.user)
        items = clean_form_data(request.POST, {'ptn': r'product_(\d+)$', 'rpl': r'\1'}, del_val=())
        orders = clean_form_data(request.POST, {'ptn': r'order_product_(\d+)$', 'rpl': r'\1'})
        cart_items = cart.cartitem_set.all()

        for key in items:
            item = cart_items.get(item=Item.objects.get(pk=to_num(key)))
            if items[key] == 0:
                item.delete()
                Item.objects.filter(pk=to_num(key)).delete()
            else:
                if item.quantity != items[key]:
                    item.quantity = items[key]
                    item.updated = datetime.datetime.now()
                    item.save()
        cart.save()

        cart_det = show_cart(request.user)
        if 'btn_save' in request.POST:
            return render(request, "orders/cart.html", 
                {'items': cart_det['items'], 'message': ['success', 'Cart saved.'], 'cart_sum': cart_det['price']})
        elif 'btn_submit' in request.POST:
            if len(orders) > 0:
                order = Order.objects.create(user=request.user, price=0)
                for key in orders:
                    item = cart_items.get(item=Item.objects.get(pk=to_num(key)))
                    OrderItem.objects.create(order=order, quantity=item.quantity, item=Item.objects.get(pk=to_num(key)))
                    order.quantity += item.quantity
                    order.price += item.item.price * item.quantity
                    item.delete()
                order.save()

            return render(request, 'orders/orders.html', 
                {'orders': Order.objects.filter(user=request.user), 'message': None})

    else:
        cart_det = show_cart(request.user)
        return render(request, "orders/cart.html", 
            {'items': cart_det['items'], 'message': None, 'cart_sum': cart_det['price']})

@login_required
def orders(request):
    if request.method == "POST":
        if any(_ in request.POST for _ in ('btn_pay', 'btn_cancel', 'btn_delete')):
            orders = clean_form_data(request.POST, {'ptn': r'order_(\d+)$', 'rpl': r'\1'})
            if 'btn_pay' in request.POST:
                raise Http404('Payment function is not available now.')
            else:
                for key in orders:
                    order = Order.objects.get(pk=to_num(key))
                    if 'btn_delete' in request.POST:
                        order_items = order.orderitem_set.all()
                        for itm in order_items:
                            Item.object.get(pk=itm.item.id).delete()
                        order.delete()
                    elif 'btn_cancel' in request.POST:
                        order.status = 'Cancelled'
                        order.updated = datetime.datetime.now()
                        order.save()

        btn = [_ for _ in ('pay', 'cancel', 'delete') if _ in request.POST]
        if len(btn) > 0:
            order_id = request.POST[btn[0]]
            if 'pay' in request.POST:
                raise Http404('Payment function is not available now.')
            else:
                order = Order.objects.get(pk=to_num(order_id))
                if 'delete' in request.POST:
                    order_items = order.orderitem_set.all()
                    for itm in order_items:
                        Item.objects.get(pk=itm.item.id).delete()
                    order.delete()
                elif 'cancel' in request.POST:
                    order.status = 'Cancelled'
                    order.updated = datetime.datetime.now()
                    order.save()
        return render(request, "orders/orders.html",
            {'orders': Order.objects.filter(user=request.user),
             'message': ['success', 'Orders modified.']})
    else:
        orders = Order.objects.filter(user=request.user)
        return render(request, "orders/orders.html",
            {'orders': orders})

@login_required
def order(request, id):
    if request.method == "POST":
        if any(_ in request.POST for _ in ('btn_save', 'btn_pay', 'btn_cancel', 'btn_delete')):
            order = Order.objects.get(pk=id)
            items = clean_form_data(request.POST, {'ptn': r'product_(\d+)$', 'rpl': r'\1'}, del_val=('0', ''))
            order_items = order.orderitem_set.all()
            order.quantity = order.price = 0
            for key in items:
                item = Item.objects.get(pk=to_num(key))
                order_item = order_items.get(item=item)
                if items[key] == 0:
                    order_item.delete()
                    item.delete()
                else:
                    if order_item.quantity != items[key]:
                        order_item.quantity = items[key]
                        order_item.updated = order.updated = datetime.datetime.now()
                        order_item.save()
                    order.quantity += items[key]
                    order.price += item.price * items[key]
            order.save()

            if 'btn_pay' in request.POST:
                raise Http404('Payment function is not available now.')
            elif 'btn_delete' in request.POST:
                order.delete()
                return redirect(reverse('orders'))
            elif 'btn_cancel' in request.POST:
                order.status = 'Cancelled'
                order.save()

            return render(request, 'orders/order.html',
                {'items': order.orderitem_set.all(), 'order': order, 'id': id,
                 'message': ['success', 'Modification saved.']})

    else:
        order = Order.objects.get(pk = id)
        return render(request, "orders/order.html", {'items': order.orderitem_set.all(), 'order': order})