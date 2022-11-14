# Django packages
from django.shortcuts import render
from django.views import View
# Local apps
from product.models import Product, Category
from product.forms import ProductSearchForm
from product.documents import ProductDocument


class HomeView(View):
    form_class = ProductSearchForm
    
    def get(self, request, category_slug=None):
        product = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            product = product.filter(category=category)
        
        # Elasticsearch
        results = {}
        if request.GET.get('search'):
            results = ProductDocument.search().query('match', name=request.GET['search'])

        context = {
            'product': product,
            'category': categories,
            'form': self.form_class,
            'results': results
        }
        return render(request, 'home/index.html', context)
