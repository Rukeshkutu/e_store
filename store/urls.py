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
    
    path('delete-item/<str:pk>/', views.delete_items, name = 'delete-item'),
    path('edit-item/<str:pk>/', views.edit_item, name = 'edit-item'),
    
    path('add-product/', views.createProduct, name = 'add-product'),
    
    #for cart
    path('update_item/', views.updateItem, name = "update_item"),
    path('cart/', views.cart, name = "cart"),
    path('check-out/', views.checkout, name = 'checkout'),
    path('process-order/', views.processOrder, name = 'process-order')
]   
