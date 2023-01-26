from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token

#forgot password
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



# Create your views here.
def admin_dashboard(request):
    return render(request, 'auth_users/admin_dashboard.html')

def staff_dashboard(request):
    return render(request, 'auth_users/staff_dashboard.html')

def user_dashboard(request):
    return render(request, 'auth_users/user_dashboard.html')


@requires_csrf_token
def dashboard(request):
    if request.user.is_superuser:
        return redirect('auth_users:admin_dashboard')
    elif request.user.is_staff:
        return redirect('auth_users:staff_dashboard')
    else:
        return redirect('auth_users:user_dashboard')
    
    
def signin_page(request):
    if request.method == 'POST':
        #username and password is taken from signin.html "name = username"
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # to make sure user exits
            user = User.objects.get(username = username)
            
        except:
            messages.error(request, 'user doesnot exit')
            
        user = authenticate(request, username= username, password = password)# to authenticate and to make sure user is currect
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('auth_users:dashboard')
            else:
                return redirect('store:items')
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
    
  
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth_users/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        "domain":'127.0.0.1:8000',
                        'site_name':'Website',
                        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token":default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    
                    messages.success(request, '')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    
    context={
        'password_reset_form': password_reset_form,
    }
    return render(request, "auth_users/password_reset.html", context)
