from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm,CustomUserChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','username','is_superuser','is_staff','last_login',)
    list_filter = ('username','is_superuser','is_staff','is_active',)
    fieldsets = (
        ('User Details',{'fields':('email','username','password',)}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions',)}),
        ('Dates',{'fields':('last_login','date_joined',)}),
    )
    add_fieldsets = (
        ('User Change Password', {
            'classes': ('wide',),
            'fields': ( 'email','username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',) 
    
admin.site.register(CustomUser,CustomUserAdmin)
    