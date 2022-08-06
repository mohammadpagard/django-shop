from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    # orders
    path('create/', views.CreateOrderView.as_view(), name='create_order'),
    path('detail/<int:order_id>', views.OrderDetailView.as_view(),
        name='order_detail'),
    # carts
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>', views.CartRemoveView.as_view(),
        name='cart_remove'),
]
