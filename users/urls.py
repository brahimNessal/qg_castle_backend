from django.urls import path, include
from .views import login_view, DishViewSet
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')
router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
] + router.urls