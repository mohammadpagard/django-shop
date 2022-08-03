from django.shortcuts import render, redirect
from django.views import View
from .models import User, OtpCode
from .forms import UserRegisterForm
from django.contrib import messages
from .forms import RegisterVerifyCodeForm
import random
from utils import send_otp_code


class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            send_otp_code(cd['phone_number'], random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'email': cd['email'],
                'full_name': cd['full_name'],
                'phone_number': cd['phone_number'],
                'password': cd['password']
            }
            messages.success(request, 'We send you a code', 'success')
            return redirect('accounts:register_verify_code')
        return redirect('home:home')


class UserRegisterVerifyCode(View):
    form_class = RegisterVerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register_verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(
                    user_session['email'],
                    user_session['full_name'],
                    user_session['phone_number'],
                    user_session['password']
                )
                code_instance.delete()
                messages.success(request, "You're registered.", 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'This code is wrong!', 'danger')
                return redirect('accounts:register_verify_code')
        return redirect('home:home')
