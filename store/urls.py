from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.items, name= 'items'),
    path('home/',views.items, name= 'items'),
    path('item/<slug:slug>/',views.item_info, name = 'product_detail' ),
#     #here slug refer to the data and category_slug is respointpoint for that data
    path('search/<slug:categroy_slug>/',views.category_list, name = 'category_list' ),
    #this url is used to view only user selected category product
   
    # path('login/', views.signin_page, name = 'signin_page'),
    # path('logout/', views.signout_page, name = 'signout_page'),
    # path('register/',views.register_page, name= 'register'),
    
    path('add-product/', views.createProduct, name = 'add-product'),
    
]
