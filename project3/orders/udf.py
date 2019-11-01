import re
from django.db import models
from django.contrib.auth.models import User
from .models import Category, Product, Topping, Addition, Item, Cart, Order, \
    ItemTopping, ItemAddition, CartItem, OrderItem


def clean_form_data(form_data, key_ptn={'ptn': r'topping_(\d+)$', 'rpl': r'\1'}, del_val=("", "0")):
    """Clean form data POST
    """
    o = dict()
    for key in form_data:
        try:
            if re.match(key_ptn['ptn'], key) and form_data[key][0] not in del_val:
                o[re.sub(key_ptn['ptn'], key_ptn['rpl'], key)] = int(form_data[key][0])
        except:
            pass
    return(o)

def to_num(txt):
    """Convert txt to num
    """
    if txt is None:
        return None
    elif txt.isdigit():
        return int(txt)
    else:
        try:
            return float(txt)
        except ValueError:
            return None

def show_cart(user):
    """Display a cart
    """
    if not isinstance(user, (User, )):
        raise TypeError("user must be a User object.")
    try:
        cart = Cart.objects.get(user=user)
        items = cart.cartitem_set.all()
        price = sum([item.quantity * item.item.price for item in items])
    except Cart.DoesNotExist:
        items = dict()
        price = 0
    return {'items': items, 'price': price}

def show_item(item):
    if not isinstance(item, (Item, )):
        raise TypeError("item must be an Item object.")
    o = {'product': item.product.id, 'price': item.price, 'topping': dict(), 'addition': dict()}
    if len(item.itemtopping_item.all()) > 0:
        for topping in item.itemtopping_item.all():
            o['topping'][str(topping.topping.id)] = topping.quantity
    if len(item.itemaddition_item.all()) > 0:
        for addition in item.itemaddition_item.all():
            o['addition'][str(addition.addition.id)] = addition.quantity
    return o
