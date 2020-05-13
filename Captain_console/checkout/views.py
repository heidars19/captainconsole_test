import json
from itertools import chain
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from account.models import User, PaymentInfo
from store.models import Product
from checkout.models import Order, OrderProduct, OrderCart


def base_context(id, context):
    context['user'] = User.objects.get(pk=id)
    # context['order_products'] = Product.objects.raw('SELECT * FROM store_product, store_orderproduct, store_order WHERE store_product.id = store_orderproduct.product_id_id  AND store_orderproduct.order_id_id = store_order.id  AND store_order.user_id_id = s%;', [id])

    # print(context)
    # context['order_products'] = Product.objects.raw('SELECT * FROM store_product, store_orderproduct, store_order WHERE store_product.id = store_orderproduct.product_id_id  AND store_orderproduct.order_id_id = store_order.id  AND store_order.user_id_id = s%;', [id])

    # Þetta er vitlaust, þarf að pulla order_id úr order_product og matcha við þetta
    # Eins og er, er þetta allavega einhver data fyrir shoppingcart
    context['order_products'] = OrderProduct.objects.filter(user_id_id=id)
    p = OrderProduct.objects.filter(user_id=id)


    if len(p) > 1 :
        for order in p :
            o = Product.objects.filter(orderproduct__ordercart__order_id=)
                # pk=order.product_id)
            OrderProduct.objects.filter(user_id_id=id, order)
            p = Order.objects.filter(ordercart__orderproduct_id__user_id=1)

    # u = User.objects.get(pk=id)
    # p = Order.objects.get('user_id_id'=id)
    # d = Product.objects.all()
    # o = Order.objects.all(user_id=1)

    # o = Order.objects.filter(user_id_id=1)
    # op = OrderProduct.objects.exclude(o.order_id_id)

    return context

 # products = Product.objects.filter(orderproduct__order_id__user_id=id)


def index(request, id=None):
    print("hello")
    context = {
        'page_checkout': 'contactinfo',
        'order_products': 'order_products',
    }
    if id != None:
        context = base_context(id, context)
    return render(request, 'checkout/index.html', context)


def shipping(request, id=None):
    context = {
        'page_checkout': 'shipping',
    }
    if id != None:
        context = base_context(id, context)
    return render(request, 'checkout/index.html', context)


@csrf_exempt
def payment(request, id=None):
    if request.method == 'POST':
        # Make sure user is logged in
        if request.session.get('user_id') is None:
            response = json.dumps({'status': 999, 'message': 'User not logged in'})
            return HttpResponse(response, content_type='application/json')

        cardHolder = request.POST.get('cardHolder')
        cardNumber = request.POST.get('cardNumber')
        expireDate = request.POST.get('expireDate')
        cvc = request.POST.get('cvc')

        PaymentInfo.insert(User.objects.get(pk=request.session.get('user_id')), cardHolder, cardNumber, expireDate, cvc)

        response = json.dumps({'status': 200, 'message': 'Yes'})
        return HttpResponse(response, content_type='application/json')

    context = {
        'page_checkout': 'paymentinfo',
    }

    if id != None:
        context = base_context(id, context)
    return render(request, 'checkout/index.html', context)


def confirmation(request, id=None):
    context = {
        'page_checkout': 'confirmation',
    }
    if id != None:
        context = base_context(id, context)
    return render(request, 'checkout/index.html', context)
