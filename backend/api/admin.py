from django.contrib import admin

from .models import Product,Category,Brand,Order,OrderITem,Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(OrderITem)
admin.site.register(Cart)
