from rest_framework import serializers
from .models import Category, Product, ProductImage, UserShoppingCart, CartItem


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    type = serializers.IntegerField()

    def create(self, validated_data):
        category = Category()
        category.name = validated_data.get('name')
        category.type = validated_data.get('type')
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.type = validated_data.get('type')
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'src',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()

    def create(self, validated_data):
        product = Product()
        product.name = validated_data.get('name')
        product.price = validated_data.get('price')
        product.category_id = validated_data.get('category_id')
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.price = validated_data.get('price')
        instance.category_id = validated_data.get('category_id')
        instance.save()
        return instance


class CartItemCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price')

    product = ProductSerializer()


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShoppingCart
        fields = ('items', 'total_price')

    items = CartItemSerializer(many=True)


