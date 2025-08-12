from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Dish

User = get_user_model()

# جرب إلغاء تسجيله فقط إذا كان مسجلاً بالفعل (بشكل آمن)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # تجاهل إذا لم يكن مسجلاً أصلاً

# الآن سجل موديل المستخدم من جديد
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'is_chef', 'is_staff', 'is_superuser')
    list_filter = ('is_chef', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    ordering = ('id',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_chef',)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('is_chef',)}),
    )

# تسجيل موديل الأطباق
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'chef', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'chef__username')
    ordering = ('-created_at',)
