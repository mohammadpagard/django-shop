from django.shortcuts import render, redirect
from django.views import View
from .models import User, OtpCode
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterVerifyCodeForm
import random
from utils import send_otp_code


class UserRegisterView(View):
	form_class = UserRegisterForm
	template_name = 'accounts/register.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form': form})

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
		return render(request, self.template_name, {'form': form})


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
				OtpCode.expired_code()
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


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'accounts/login.html'

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			# get user fields
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(request, email=email, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				return redirect('home:home')
			messages.error(request, "You're email or password is wrong", 'danger')
		return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.info(request, 'You logged out is successfully', 'info')
		return redirect('home:home')
