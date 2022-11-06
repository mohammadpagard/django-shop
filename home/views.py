# Django packages
from django.shortcuts import render
from django.views import View
from django.db.models import Q
# Local apps
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


def search(request):
    search_product = request.GET.get('search')
    if search_product:
        products = Product.objects.filter(
            Q(name__icontains=search_product) & Q(description__icontains=search_product)
        )
    else:
        products = Product.objects.all().order_by("-created")
    
    context = {'product': products}
    return render(request, 'home/index.html', context)
