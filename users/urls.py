from django.urls import path, include
from .views import login_view, DishViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]