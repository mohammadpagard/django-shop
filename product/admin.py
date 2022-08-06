from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created')
    list_filter = ('created', 'available')
    search_fields = ('name', 'description')
    raw_id_fields = ('category',)


admin.site.register(Category)
