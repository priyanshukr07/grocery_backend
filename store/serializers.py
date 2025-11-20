from rest_framework import serializers
from .models import User, Category, Product, CartItem, Order, OrderItem, WishlistItem, PromoCode, ProductImage
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id','username','email','password','first_name','last_name']
        # Removed role from fields so public cannot set it

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.role = "customer"  # force customer role ALWAYS
        user.save()
        return user

class ManagerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.role = "manager"     # assign manager role
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

    def validate_name(self, value):
        name_upper = value.upper()
        if Category.objects.filter(name=name_upper).exists():
            raise serializers.ValidationError("Category already exists.")
        return name_upper
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Category.objects.all(), source='category')
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id","name","slug","category","category_id","price","stock","created_at","images"]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(), source='product')
    class Meta:
        model = CartItem
        fields = ['id','user','product','product_id','quantity','added_at']
        read_only_fields = ('user','added_at')

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(), source='product')
    class Meta:
        model = WishlistItem
        fields = ['id','user','product','product_id','added_at']
        read_only_fields = ('user','added_at')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','customer','created_at','total_amount','items']
        read_only_fields = ('customer','created_at','total_amount','items')

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
