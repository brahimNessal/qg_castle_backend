from rest_framework import serializers
from .models import Dish

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
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
