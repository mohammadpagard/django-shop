from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Password don't match")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change password using <a href=\"../password/\">this form</a>"
        )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'full_name',
            'phone_number',
            'is_active',
            'is_admin'
            )


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(
        label='Fullname',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('This email already exists!')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number)
        if user:
            raise ValidationError('This phone number already exists!')
        # Removed the duplicate code for this phone number
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number


class RegisterVerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
