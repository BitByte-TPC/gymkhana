from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Student, Faculty, Staff


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email','first_name', 'last_name', 'contact_no', 'user_type', 'is_staff', 'is_active',)
    list_filter = ('email','first_name', 'last_name', 'contact_no', 'user_type', 'is_staff', 'is_active',)
    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('User Info', {'fields': ('first_name', 'last_name', 'gender','contact_no', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'gender','contact_no', 'user_type', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'roll_no', 'batch', 'bio', 'linkedin', 'facebook', 'instagram', 'github')
# Register your models here

admin.site.register(get_user_model(), CustomUserAdmin)
# admin.site.register(Student)
# admin.site.register(Faculty)
# admin.site.register(Staff)
