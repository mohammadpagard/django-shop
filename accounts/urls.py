from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('register-verify/',
        views.UserRegisterVerifyCode.as_view(), name='register_verify_code'),
]
