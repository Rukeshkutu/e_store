from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
import os
# # Create your views here.
from .models import *

def items(request):
    products = Product.objects.all() #this query is equivalent in sql as select all products 
    #add paginator in our site
    paginator = Paginator(products, 3) # Show 25 contacts per page.

    page_number = request.GET.get('page')#get page number from url page
    page_obj = paginator.get_page(page_number)
    
    #here we only add page_obj in the dictionary because we want to only show three product at one page not all product
    #and have to make changes in the for loop of home.html so instead of all product only three product is shown
    context = {'page_obj': page_obj}#
    # context = {'products':products}
    return render(request, 'store/home.html', context)
    
#     #render is used for loading templates/gatheiring of data
#     #{products:'products'} is the data we want to display in template

def categories(request):
    return{
        'categories': Category.objects.all()
        #if you want to make categories available in every single page then we need to add ''store.views.categories''in templates in setting
    }
    
    
def item_info(request, slug):
    product = get_object_or_404(Product, slug = slug, in_stock = True)
    
    context = {'product':product}
    return render(request, 'store/detail.html', context)


def category_list(request, categroy_slug):
    category  = get_object_or_404(Category, slug = categroy_slug)#slug for one item form the database
    products = Product.objects.filter(category = category)#this will filter the category of the said product
    # Show 25 contacts per page.
    paginator = Paginator(products, 3) 
    page_number = request.GET.get('page')
    #get page number from url page
    page_obj = paginator.get_page(page_number)
    
    
    context = {'category': category,'page_obj': page_obj}
    return render(request, 'store/category.html', context)


def createProduct(request):
    
    form = ProductForm()#improt productform form form.py
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)#request.File send request to the file to be uploaded to uploade the file, without it there would be error while saving file
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

def delete_items(request, pk):
    item = Product.objects.get(id = pk)
    
    # if request. != item.created_by:
    #     messages.INFO(request, 'You are not authorized')
    
    if request.method == 'POST':
        item.delete()
        return redirect('store:items')

    context = {
        'item':item
    }
    return render(request, 'store/delete.html', context)
# @login_required  


def edit_item(request, pk):
    item = Product.objects.get(id = pk) # we need to pass id in the url for edit in createproduct.html
    form = ProductForm(instance= item) 
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(item.image) > 0:
                os.remove(item.image.path)
            item.image = request.FILES['image']
        form.save()
        return redirect('store:items')
        messages.success(request, 'Item updated successfully')
    context = {'form':form}
    return render(request, 'store/createproduct.html', context)
