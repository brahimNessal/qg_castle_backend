from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from .models import Ingredient
from .serializers import IngredientSerializer
from .permissions import IsChefForWrite, IsPurchaserForRead


from .models import Dish
from .serializers import DishSerializer

@api_view(['POST'])
def login_view(request):
    print("====== LOGIN VIEW CALLED ======")
    print("Headers:", request.headers)
    print("Body:", request.body)
    print("Parsed Data:", request.data)

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Missing credentials'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_chef': user.is_chef,
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # تمرير request للـ Serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        if not self.request.user.is_chef:
            raise PermissionDenied("Only chefs can add dishes.")

        today = timezone.now().date()
        dish_name = serializer.validated_data['name']
    
        existing_dish = Dish.objects.filter(
            name=dish_name,
            created_at__date=today,
            chef=self.request.user
        ).first()

        if existing_dish:
            existing_dish.quantity += 1
            existing_dish.save()
        else:
            serializer.save(chef=self.request.user)

    def get_queryset(self):
        today = timezone.now().date()
        return Dish.objects.filter(created_at__date=today).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        dish = self.get_object()
        if not request.user.is_chef or dish.chef != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        dish.quantity += 1
        dish.save()
        return Response({'status': 'quantity increased', 'quantity': dish.quantity})

    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        dish = self.get_object()
        if dish.quantity > 0:
            dish.quantity -= 1
            dish.save()
            return Response({'status': 'quantity decreased', 'quantity': dish.quantity})
        return Response({'error': 'Quantity is already zero'}, status=400)
    
class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all().order_by('-created_at')
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated, IsChefForWrite, IsPurchaserForRead]

    def get_queryset(self):
        user = self.request.user

        # القراءة (GET/HEAD/OPTIONS): للمسؤول عن الشراء فقط
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            if getattr(user, 'is_staff', False):      # أو is_purchaser
                return Ingredient.objects.all().order_by('-created_at')
            # منع الطباخ من رؤية الجدول (حسب شرطك)
            return Ingredient.objects.none()

        # الكتابة: لا نحتاج queryset خاص؛ سنعتمد على صلاحيات الكائن في التعديل/الحذف
        return Ingredient.objects.all()

    def destroy(self, request, *args, **kwargs):
        # لا يحذف إلا مالك السجل (مغطى في IsChefForWrite.object)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # لا يحدّث إلا مالك السجل
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


