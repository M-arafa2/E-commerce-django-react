from django_filters import rest_framework
from .models import Product
class ProductFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__name', lookup_expr='iexact')
    brand = rest_framework.CharFilter(field_name='brand__brand', lookup_expr='iexact')
    class Meta:
        fields = ("category","brand","name",)
        model = Product