from django.shortcuts import render
from django.views import View
from product.models import Product


class HomeView(View):
    def get(self, request):
        product = Product.objects.filter(available=True)
        return render(request, 'home/index.html', {'product': product})
