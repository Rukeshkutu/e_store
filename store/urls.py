from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.all_products, name= 'all_products'),
    path('home/',views.all_products, name= 'all_product'),
    path('item/<slug:slug>/',views.product_detail, name = 'product_detail' ),
    #here slug refer to the data and category_slug is respointpoint for that data
    path('search/<slug:categroy_slug>/',views.category_list, name = 'category_list' ),
    #this url is used to view only user selected category product
   
    path('login/', views.signin_page, name = 'signin_page'),
    path('logout/', views.signout_page, name = 'signout_page'),
    path('register/',views.register_page, name= 'register'),
    
    path('add-product/', views.createProduct, name = 'add-product'),
    
]
