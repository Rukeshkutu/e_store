from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import *

def all_products(request):
    products = Product.objects.all() #this query is equivalent in sql as select all products 
    context = {'products':products}

    return render(request, 'store/home.html', context)
    #render is used for loading templates/gatheiring of data
    #{products:'products'} is the data we want to display in template

def categories(request):
    return{
        'categories': Category.objects.all()#if you want to make categories available in every single page then we need to add ''in templates in setting
    }
    
    
def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug, in_stock = True)
    
    context = {'product':product}
    return render(request, 'store/detail.html', context)


def category_list(request, categroy_slug):
    category  = get_object_or_404(Category, slug = categroy_slug)#slug for one item form the database
    products = Product.objects.filter(category = category)#this will filter the category of the said product
    
    context = {'category': category, 'products':products}
    return render(request, 'store/category.html', context)