from rest_framework import serializers
from .models import Dish

class DishSerializer(serializers.ModelSerializer):
    chef_username = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'image', 'quantity', 'chef', 'chef_username', 'created_at')
        read_only_fields = ['id','chef', 'chef_username', 'created_at']

    def get_chef_username(self, obj):
        return obj.chef.username