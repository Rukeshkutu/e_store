from django.shortcuts import render

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