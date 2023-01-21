from django.shortcuts import render, get_object_or_404,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
from django.contrib import messages
from .utils import cartData, cookieCart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import json, datetime
from django.db.models import Q
from .forms import *
import os
# # Create your views here.
from .models import *

def items(request): 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    else:
        items =[]
        order = {'get_cart_total': 0, 'get_cart_items':0 }
        cartItems = order['get_cart_items']
        
    products = Product.objects.all()
    
    #To show items per page
    paginator = Paginator(products, 3) # 

    page_number = request.GET.get('page')#get page number from url page
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'cartItems':cartItems}#
    # context = {'products':products}
    return render(request, 'store/home.html', context)
    
    
def categories(request):
    return{
        'categories': Category.objects.all()
    }
    

def search(request):
    #query' is from navbar.html line 42
    queries = request.GET.get('query', False)
    
    if len(queries) > 50:
        product = Product.objects.none()
    else:
        product = Product.objects.filter(title__icontains = queries)
    
    
    if product.count() == 0:
        messages.warning(request, 'Search result not found.Please search again.')
    
    paginator = Paginator(product, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'queries':queries 
    }
    return render(request, 'store/search.html', context)
        
        
def item_detail(request, slug):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items =[]
        order = {'get_cart_total': 0, 'get_cart_items':0 }
        cartItems = order['get_cart_items']
        
    product = get_object_or_404(Product, slug = slug, in_stock = True)
    
    context = {'product':product, 'cartItems': cartItems}
    return render(request, 'store/detail.html', context)


def category_list(request, categroy_slug):
    category  = get_object_or_404(Category, slug = categroy_slug)
    products = Product.objects.filter(category = category)
   
    paginator = Paginator(products, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {'category': category,'page_obj': page_obj}
    return render(request, 'store/category.html', context)

@login_required
def addProduct(request,pk=None):
    #from form.py
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            messages.success(request, 'product added succcssfully')
            return redirect('store:items')
        else:
            messages.error(request, 'Failed to add Product')
    
    context = {
        'form':form
    }
    return render(request, 'store/createproduct.html', context)

@login_required
def delete_items(request, pk):
    item = Product.objects.get(id = pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('store:items')

    context = {
        'item':item
    }
    return render(request, 'store/delete.html', context)
 

@login_required
def edit_item(request, pk):
    item = Product.objects.get(id = pk)
    form = ProductForm( request.POST or None, request.FILES or None, instance = item)
    if request.method == 'POST':
        if form.is_valid():
            old_image = item.image
            item = form.save()
            if item.image != old_image:
                default_storage.delete(old_image.path)
            # form.save()
            return redirect('store:items')
    # if request.method == 'POST'and form.is_valid():
    #     if len(request.FILES) != 0:
    #         if len(item.image) > 0:
    #             os.remove(item.image.path)
    #         item.image = request.FILES['image']
    #     form.save()
    #     return form.cleaned_data
    #     # return redirect('store:items')
    #     messages.success(request, 'Item updated successfully')
    context = {'form':form}
    return render(request, 'store/createproduct.html', context)

@login_required
def cart(request):
    # if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    
    if request.user.is_authenticated is None:
        return redirect('auth_users:signin_page')
    
    # else:
    #     return redirect('auth_users:signin_page')
     
    products = Product.objects.all()
    context = {'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
    # if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    # else:
    #     return redirect('signin_page')
     
    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)



# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
#for cart
def updateItem(request):
    data = json.loads(request.body)# to add data we import jason we gone a parse a data in request.body
    productId = data['productId']#get some value from actiona and priductid from cart.js
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer#crateing customer and querying customer
    product = Product.objects.get(id=productId)#get product from the  id we are passing
    order, created = Order.objects.get_or_create(customer=customer, complete=False)#here creating or adding order
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # if order of product is already exist then below loop runs
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)#if the product is added to cart the in the cartlogo in home page show increase in number
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item was added', safe = False)

#for payment process
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:     
        customer = request.user.customer	
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:	
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])#here form and total is taken from checkout.html line 151 for form and 118 for total
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
        order.save()
     
    if order.shipping == True:     
        ShippingAddress.objects.create(	
            customer=customer,	    
            order=order,	
            address=data['shipping']['address'],	
            city=data['shipping']['city'],	
            state=data['shipping']['state'],	
            zipcode=data['shipping']['zipcode'],	
        )      
