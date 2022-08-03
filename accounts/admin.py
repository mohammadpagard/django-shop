from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User, OtpCode


# Customizing user model admin
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name', 'email', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Personal info', {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email', 'phone_number')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')
    list_filter = ('phone_number', 'created')
