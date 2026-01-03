import django_filters 
from .models import RentSpace
from django_filters import rest_framework as filters

class RentSpaceFilter(filters.FilterSet):
    rent_min = django_filters.NumberFilter(field_name='rent', lookup_expr='gte')
    rent_max = django_filters.NumberFilter(field_name='rent', lookup_expr='lte')
    district = django_filters.CharFilter(lookup_expr='iexact')
    street = django_filters.CharFilter(field_name='street_address', lookup_expr='icontains')
    state = django_filters.CharFilter(field_name='state', lookup_expr='iexact')
class Meta:
    model = RentSpace
    fields = ['is_occupied','state','country','district','rent_min', 'rent_max']

