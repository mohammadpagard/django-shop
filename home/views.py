# Django packages
from django.shortcuts import render
from django.views import View
# Third party apps
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
# Local apps
from product.models import Product, Category
from product.forms import ProductSearchForm


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
            s = Search(index="product")
            first_filter = Q("fuzzy", name=request.GET['search']) | Q("fuzzy", description=request.GET['search'])
            results = s.filter('bool', filter=[first_filter])

        context = {
            'product': product,
            'category': categories,
            'form': self.form_class,
            'results': results
        }
        return render(request, 'home/index.html', context)
