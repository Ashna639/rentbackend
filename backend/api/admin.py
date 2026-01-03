from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import RentSpace
from django.utils.html import format_html
from django.urls import reverse

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_seller', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_seller', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    actions = ['make_seller', 'make_consumer', 'activate_users', 'deactivate_users']
    
    def make_seller(self, request, queryset):
        updated = queryset.update(is_seller=True)
        self.message_user(request, f'{updated} users made sellers.')
    make_seller.short_description = "Mark as Seller"
    
    def make_consumer(self, request, queryset):
        updated = queryset.update(is_seller=False)
        self.message_user(request, f'{updated} users made consumers.')
    make_consumer.short_description = "Mark as Consumer"
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')
    deactivate_users.short_description = "Deactivate selected users"

@admin.register(RentSpace)
class RentSpaceAdmin(admin.ModelAdmin):
    list_display = ['space_type', 'owner', 'rent', 'deposit', 'is_occupied', 'district']
    list_filter = ['is_occupied', 'space_type', 'district', 'state', 'owner__is_seller']
    search_fields = ['space_type', 'street_address', 'owner__username']
    list_per_page = 20
    actions = ['mark_occupied', 'mark_vacant']  # ✅ FIXED: List only
    
    def owner(self, obj):
        return obj.owner.username if obj.owner else "No Owner"
    owner.short_description = "Seller"
    owner.admin_order_field = 'owner__username'
    
    def mark_occupied(self, request, queryset):
        updated = queryset.update(is_occupied=True)
        self.message_user(request, f'{updated} spaces marked occupied.')
    mark_occupied.short_description = "Mark as Occupied"
    
    def mark_vacant(self, request, queryset):
        updated = queryset.update(is_occupied=False)
        self.message_user(request, f'{updated} spaces marked vacant.')
    mark_vacant.short_description = "Mark as Vacant"
