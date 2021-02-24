from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Customer, Shop, Product, Order

import uuid


def is_vip(customer_id):
    """Extract customer vip information
    """
    customer = Customer.objects.get(customer_id=customer_id)
    return customer.vip


def verify_cusomter(func):
    """Verify customer have vip identity
    """
    def wrapper(request, *args, **kwargs):
        customer_id = request.POST.get('customer_id')
        product = Product.objects.get(
            product_id=request.POST.get('product_id'))
        if product.vip and not is_vip(customer_id):
            return HttpResponseBadRequest("Customer not vip")
        return func(request, *args, **kwargs)
    return wrapper


def verify_product_qty(func):
    """Verify product id and qty have enough qty to support action
    """
    def wrapper(request, *args, **kwargs):
        product_qty = request.POST.get('product_qty')
        product = Product.objects.get(
            product_id=request.POST.get('product_id'))
        if int(product_qty) > product.stock_pcs:
            return HttpResponseBadRequest('庫存不足')
        return func(request, product)
    return wrapper


def check_customer(request, customer_id):
    """Check the vip identification of customer
    """
    return is_vip(customer_id)


def index(request):
    """Povide product/order information list
    """
    try:
        # query all of product and order
        product_list = Product.objects.all()
        order_list = Order.objects.all()
        # collect in context
        context = {
            'product_list': product_list,
            'order_list': order_list,
        }

        return render(request, 'dashboard/index.html', context)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product does not exist")
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order does not exist")
    except Exception:
        raise


@verify_cusomter
@verify_product_qty
def create_order(request, product):
    """Create order
    """
    try:
        product_qty = int(request.POST.get('product_qty'))
        Order.objects.create(
            order_id=str(uuid.uuid4()),
            product_id=product.product_id,
            qty=product_qty,
            price=product.price*product_qty,
            shop_id=product.shop_id.shop_id,
            customer_id=request.POST.get('customer_id')
        )

        # if order success, should update product qty
        updated_product = Product.objects.get(product_id=product.product_id)
        updated_qty = updated_product.stock_pcs - product_qty

        Product.objects.filter(product_id=product.product_id).update(
            stock_pcs=updated_qty)

        return HttpResponseRedirect(reverse('dashboard:index'))
    except Exception:
        raise


def delete_order(request, order_id):
    """Delete order
    """
    try:
        # delete order
        deleted_order = Order.objects.get(order_id=order_id)
        product_info = {
            'product_id': deleted_order.product_id,
            'product_qty': deleted_order.qty
        }
        Order.objects.filter(order_id=order_id).delete()

        # update product stock_pcs
        updated_product = Product.objects.get(
            product_id=product_info.get('product_id'))
        updated_qty = product_info.get(
            'product_qty') + updated_product.stock_pcs
        Product.objects.filter(product_id=product_info.get(
            'product_id')).update(stock_pcs=updated_qty)

        return HttpResponseRedirect(reverse('dashboard:index'))
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order does not exist")
    except Exception:
        raise
