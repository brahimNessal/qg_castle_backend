from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsChefForWrite(BasePermission):
    """
    يسمح بالإنشاء/التعديل/الحذف للطباخ فقط.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # سنمنع القراءة هنا للطباخ، ونفصلها في IsPurchaserForRead
            return True
        # كتابة: لازم يكون طباخ
        return bool(getattr(request.user, 'is_chef', False))

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # لا يعدّل إلا مالك السجل (الطباخ الذي أدخله)
        return obj.chef_id == request.user.id


class IsPurchaserForRead(BasePermission):
    """
    يسمح بالقراءة فقط للمسؤول عن الشراء.
    سنستخدم is_staff كمؤشر للمسؤول (أو يمكنك تبديله لاحقًا إلى is_purchaser).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated and request.user.is_staff)
        return True  # يُترك قرار الكتابة لـ IsChefForWrite
