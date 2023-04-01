from django.db import models

# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
import os
from datetime import datetime
from django.contrib.auth.models import User
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand

def content_file_name(instance, filename):
        ext = filename.split('.')[-1]
        print(datetime.now().strftime("%H-%M-%S"))
        filename = "%s_%s_%s%s.%s" % (instance.id,datetime.now().date(), datetime.now().strftime("%H-%M-%S"), "/preview/", ext)
        return os.path.join('images', filename)
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    preview_img =models.ImageField(null=True,blank=True,upload_to=content_file_name)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True,max_length=1000)
    details = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100,null=True,blank=True)
    stock_qty = models.IntegerField()

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_together =('product','user')
        
# model for the whole order list 
# linked to user who ordered and to delivery crew
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="delivery_crew",null=True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)
    
# model for single item in the order list
# relationship with order and menu item models 
class OrderITem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="Order")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_together =('order','product')
    
