from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.
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
            return redirect('store:items')#when user is login page is redirectd to home.html page through url
        else:
            messages.error(request, 'user name or email doesnot exist')
    
    context ={
        
    }
    return render(request, 'auth_users/signin.html', context)

def signout_page(request):
    logout(request)#this delete the token so it delete the user
    return redirect("store:items")

def register_page(request):  
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'user created successfully')
            return redirect('signin_page')
    else:
        form = SignUpForm()
        
    context = {
        'form':form
    }
    return render(request, 'auth_users/register.html', context)
    
  

