from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Dish
from .models import User

User = get_user_model()

# جرب إلغاء تسجيله فقط إذا كان مسجلاً بالفعل (بشكل آمن)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # تجاهل إذا لم يكن مسجلاً أصلاً

# الآن سجل موديل المستخدم من جديد
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_chef'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_chef')
    search_fields = ('username', 'email')
    ordering = ('id',)

    # أضف is_chef فقط، والباقي already موجود
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
