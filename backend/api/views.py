from django.shortcuts import render
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from .models import Order,Product,Category,OrderITem,Cart
from .serializers import ProductSerializer,CategorySerializer,OrderItemSerializer,OrderSerializer,cartSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .filters import ProductFilter
from django.contrib.auth.models import User
# Create your views here.
@extend_schema(responses=ProductSerializer)
class ProductView(generics.ListAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    filterset_class = ProductFilter
    
@extend_schema(responses=ProductSerializer)
class SingleProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
@extend_schema(responses=CategorySerializer)
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
    
#CART AND ORDERS
@extend_schema(responses=cartSerializer)
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("Deleted")
    
@extend_schema(responses=OrderSerializer)
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
         Cart.objects.all().filter(user =self.request.user)
        
    def create(self, request, *args, **kwargs):
        product_count = Cart.objects.all().filter(user=self.request.user).count()
        if product_count == 0:
            return Response({"message:": "cart is empty"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        print(order_serializer)
        print(data)
        tr = True
        if (order_serializer.is_valid()):
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderITem(
                    order=order,
                    product_id=item['product_id'],
                    unit_price =item['unit_price'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()
                Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

            result = order_serializer.data.copy()
            result['total'] = total
            
            return Response(order_serializer.data)
        #return Response({"message":"please enter valid data"})
    
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total

@extend_schema(responses=OrderSerializer)
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if IsAdminUser: 
            return super().update(request, *args, **kwargs)
        else: #Super Admin, Manager and Delivery Crew
            # customer
            return Response('Not Ok')