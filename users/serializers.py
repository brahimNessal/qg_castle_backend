from rest_framework import serializers
from .models import Dish
from .models import Ingredient

class DishSerializer(serializers.ModelSerializer):
    chef_username = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'image', 'image_url', 'quantity', 'chef', 'chef_username', 'created_at')
        read_only_fields = ['id','chef', 'chef_username', 'created_at']

    def get_chef_username(self, obj):
        return obj.chef.username

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
            request = self.context.get('request')
            
            # إذا الرابط مش كامل، يكمله بالـ domain
            if request and not url.startswith('http'):
                url = request.build_absolute_uri(url)
            return url
        return None

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'price_per_unit', 'total_price', 'chef', 'created_at']
        read_only_fields = ['id', 'total_price', 'chef', 'created_at']

    def create(self, validated_data):
        # اربط المكوّن بالطباخ الذي أضافه
        request = self.context['request']
        validated_data['chef'] = request.user
        return super().create(validated_data)

