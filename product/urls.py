from django.urls import path
from . import views


app_name = 'product'
urlpatterns = [
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
]
