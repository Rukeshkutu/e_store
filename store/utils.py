import json
from . models import *


def cookieCart(request):
    #Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('cart:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:#here is the logic if user want to put item in cart being unauthenticated
        try: #here try and extcept is for if we delete item then it should pass
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL': product.imageURL
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    return{'cartItems':cartItems, 'order':order, 'items':items}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)#shows the number of item in the cart 
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems':cartItems, 'order':order, 'items':items}

# def guestOrder(request, data):
#     print('user is not logged in ......')
#     print('cookies:', request.COOKIES)
#     name = data['form']['name']
#     email = data['form']['email']
    
#     cookieData = cookieCart(request)
#     items = cookieData['items']
    
#     customer, created = Customer.objects.get_or_create(
#         email = email,
#     )
#     customer.name = name
#     customer.save()

#     order = Order.objects.create(
#         customer=customer,
#         complete=False,
#     )

#     for item in items:
#         product = Product.objects.get(id = item['product']['id'])

#         orderItem = OrderItem.objects.create(
#             product=product,
#             order=order,
#             quantity = item['quantity']
#         )

#     return customer, order
