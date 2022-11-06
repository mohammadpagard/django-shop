from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search, name='search-products'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
]
