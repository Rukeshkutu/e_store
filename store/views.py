from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .forms import *
# Create your views here.
from .models import *

def all_products(request):
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
    
    #render is used for loading templates/gatheiring of data
    #{products:'products'} is the data we want to display in template

def categories(request):
    return{
        'categories': Category.objects.all()
        #if you want to make categories available in every single page then we need to add ''store.views.categories''in templates in setting
    }
    
    
def product_detail(request, slug):
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


def signin_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')#here username should be same as the  "name = 'username '" in signin.html
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)#'username = username' is to make sure user exite
            
        except:
            messages.error(request, 'user doesnot exit')#flash messages
            
        user = authenticate(request, username= username, password = password)# to authenticate and to make sure user is currect
        if user is not None:
            login(request, user)
            return redirect('store:all_products')#when user is login page is redirectd to home.html page through url
        else:
            messages.error(request, 'user name or email doesnot exist')
    
    context ={
        
    }
    return render(request, 'store/signin.html', context)

def signout_page(request):
    logout(request)#this delete the token so it delete the user
    return redirect("store:all_products")

# def signup_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if password == confirm_password:
#             if User.objects.filter(username = username).exists():
#                 messages.info(request, 'User name already exist')
#                 return redirect('store:signup_page')
#             else:
#                 user = User.objects.create_user(username= username, password = password, email= email)
#                 user.set_password(password)
#                 # user.is_staff = True
#                 user.save()
#                 messages.info(request, 'success')
#                 return redirect('store:signin_page')
#         else:
#             messages.error(request, "password doesnot match")
#             return redirect('store:signup_page')
            
#     else:
#         context ={
            
#         }
#         return render(request, 'store/signup.html', context)


def register_page(request):  
    if request.POST == 'POST':  
        form = CustomUserCreationForm()  
        if form.is_valid():  
            form.save()  
    else:  
        form = CustomUserCreationForm()  
    context = {  
        'form':form  
    }  
    return render(request, 'store/register.html', context)


def createProduct(request):
    form = ProductForm()#improt productform form form.py
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:all_products')
    
    context = {
        'form':form
    }
    return render(request, 'store/createproduct.html', context)

