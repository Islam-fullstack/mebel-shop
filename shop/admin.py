from django.contrib import admin
from .models import Category, Product, Review, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_featured', 'is_available']
    list_filter = ['category', 'material', 'is_featured', 'is_available']
    list_editable = ['price', 'stock', 'is_featured', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    inlines = [OrderItemInline]

admin.site.site_header = "Mebel Do'kon Boshqaruvi"
admin.site.site_title = "Mebel Admin"
