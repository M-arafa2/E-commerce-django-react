from django.urls import path
from . import views

urlpatterns = [
    #path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('product/', views.ProductView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
    path('product/<int:pk>', views.SingleProductView.as_view()),
]