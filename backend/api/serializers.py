from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Category,Order,OrderITem,Cart,Product,Brand
from decimal import Decimal
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = ['name']
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model= Brand
        fields = ['brand']
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset = Category.objects.all(),
        slug_field='name'
    )
    brand = serializers.SlugRelatedField(
        queryset = Brand.objects.all(),
        slug_field='brand'
    )
    class Meta:
        model = Product
        fields = ['name','preview_img','brand','category','description','details',
                  'price','sku','stock_qty']
        
class cartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    def validate(self, attrs):
        product = get_object_or_404(Product,name = attrs['product'])
        attrs['unit_price'] = product.price
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return super().validate(attrs)
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity', 'unit_price', 'price']
        extra_kwargs ={
            'price':{'read_only':True},
            'unit_price':{'read_only':True}
               
        }
       
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderITem
        fields = ['order', 'product', 'quantity',
                  'unit_price', 'price'] 
        
class OrderSerializer(serializers.ModelSerializer):
    orderItem = OrderItemSerializer(many = True, read_only = True,
                                    source ='Order')
    class Meta:
        model  = Order
        fields = ['id', 'user', 'delivery_crew', 'status',
                  'total', 'date', 'orderItem']
        extra_kwargs ={
            'total':{'read_only':True},
            'date':{'read_only':True},
            'user':{'read_only':True},     
        }
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        

    