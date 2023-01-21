from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def admin_dashboard(request):
    return render(request, 'auth_users/admin_dashboard.html')

def staff_dashboard(request):
    return render(request, 'auth_users/staff_dashboard.html')

def user_dashboard(request):
    return render(request, 'auth_users/user_dashboard.html')
@csrf_exempt()
def dashboard(request):
    if request.user.is_superuser:
        return redirect('auth_users:admin_dashboard')
    elif request.user.is_staff:
        return redirect('auth_users:staff_dashboard')
    else:
        return redirect('auth_users:user_dashboard')
    
    
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
            if request.user.is_superuser:
                return redirect('auth_users:dashboard')
            else:
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
    
  

