from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Faculty, Staff, Student, StudentSocial, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'contact_no',
        'user_type',
        'is_staff',
        'is_superuser'
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'contact_no',
        'user_type',
        'is_staff',
        'is_superuser'
    )
    list_filter = (
        'email',
        'first_name',
        'last_name',
        'contact_no',
        'user_type',
        'is_staff',
        'is_superuser'
    )
    ordering = ('email',)
    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('User Info', {'fields': ('first_name', 'last_name', 'gender', 'contact_no', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None,
            {
                'classes': ('wide'),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'gender',
                    'contact_no',
                    'user_type',
                    'is_staff',
                    'is_active'
                )
            })
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'batch', 'department', 'hostel_address')
    search_fields = ('user', 'roll_no', 'batch', 'department', 'hostel_address')
    list_filter = ('user', 'roll_no', 'batch', 'department', 'hostel_address')
    ordering = ('-user__date_joined',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'department', 'designation')
    search_fields = ('user', 'title', 'department', 'designation')
    list_filter = ('user', 'title', 'department', 'designation')
    ordering = ('-user__date_joined',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation')
    search_fields = ('user', 'department', 'designation')
    list_filter = ('user', 'department', 'designation')
    ordering = ('-user__date_joined',)


@admin.register(StudentSocial)
class StudentSocialAdmin(admin.ModelAdmin):
    list_display = ('user', 'github', 'twitter', 'linkedin', 'instagram', 'facebook')
    search_fields = ('user', 'github', 'twitter', 'linkedin', 'instagram', 'facebook')
    list_filter = ('user', 'github', 'twitter', 'linkedin', 'instagram', 'facebook')
    ordering = ('-user__date_joined',)
