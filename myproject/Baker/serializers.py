from rest_framework import serializers
from .models import *

class BakerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Baker
        fields = (
            'id',
            'name',
            'email',
            'location',
            'phoneNumber',
            'image',
            'is_active',
        )

class BakerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baker
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class BakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baker
        fields =  ["name", "location", "phoneNumber" , "location","image","email"]

class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'


class BakerWithUserIdSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Baker
        fields = '__all__'

from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'datetime', 'product', 'product_name', 'product_price', 'product_image']

    def get_product_name(self, obj):
        return obj.product.cakeName

    def get_product_price(self, obj):
        return obj.product.price

    def get_product_image(self, obj):
        return obj.product.image.url
