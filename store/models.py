from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE 
#reverse is a tool that give us to build an url
from django.urls import reverse
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='customer', null = True, blank=True)
    name = models.CharField(max_length=100, null = True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length = 100,unique=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        
    def get_absolute_url(self):#for dynamic link for category
        return reverse('store:category_list', args=[self.slug])
        
    def __str__(self):
        return self.name
    
    
        
class Product(models.Model):
    category = models.ForeignKey(Category,related_name='product', on_delete=models.CASCADE)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_name')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'images/')
    slug = models.SlugField(max_length=100)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Product'
        ordering = ('-created', )
        
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def __str__(self):
        return self.title
   
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)# many to one relationship
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False) # if complete is false that mean it is open cart, can continue to add items to that cart
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):		
        shipping = False		
        orderitems = self.orderitem_set.all()		
        for i in orderitems:		
        	# if i.product.digital == False:		
        	shipping = True		
        return shipping

    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
      #  return self.product
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) 
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



    