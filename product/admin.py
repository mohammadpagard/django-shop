from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created')
    list_filter = ('created', 'available')
    search_fields = ('name', 'description')
    raw_id_fields = ('category',)
    prepopulated_fields = {'slug': ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub')
    list_filter = ('is_sub',)
    search_fields = ('name',)
    raw_id_fields = ('sub_category',)
    prepopulated_fields = {'slug': ('name',)}
