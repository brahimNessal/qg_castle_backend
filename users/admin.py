from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Dish, User

User = get_user_model()

# إلغاء التسجيل القديم إذا كان موجود
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'is_chef', 'is_ingredient_manager', 'is_staff', 'is_superuser')
    list_filter = ('is_chef', 'is_ingredient_manager', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    ordering = ('id',)

    # fieldsets الأصلي فيه is_staff, is_superuser إلخ
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_chef', 'is_ingredient_manager')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_chef', 'is_ingredient_manager', 'is_staff', 'is_superuser'),
        }),
    )


# تسجيل الأطباق
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'chef', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'chef__username')
    ordering = ('-created_at',)
