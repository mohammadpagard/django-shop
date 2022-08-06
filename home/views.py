from django.shortcuts import render
from django.views import View
from product.models import Product, Category


class HomeView(View):
    def get(self, request, category_slug=None):
        product = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            product = product.filter(category=category)

        return render(request, 'home/index.html', {
            'product': product,
            'category': categories
        })
