from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Category, CartItem, WishlistItem, Order, OrderItem, PromoCode, ProductImage
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer, WishlistItemSerializer, OrderSerializer, UserSerializer, ManagerCreateSerializer, PromoCodeSerializer, ProductImageSerializer
from .permissions import IsManagerOrReadOnly, IsManager, IsAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F, Count
from rest_framework import generics
from django.utils import timezone
from django.http import Http404
from rest_framework import serializers
from django.db.models import Prefetch
from django.utils.text import slugify
from django.db.models.functions import Coalesce

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CreateManagerView(generics.CreateAPIView):
    serializer_class = ManagerCreateSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save(role="manager")
  
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]
    
    def get_object(self):
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        try:
            return Category.objects.get(slug=slug, id=pk)
        except Category.DoesNotExist:
            raise Http404("Category not found")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_object(self):
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        obj = Product.objects.filter(slug=slug, id=pk).first()
        if not obj:
            raise Http404("No product matches given slug and id")
        return obj

    def get_queryset(self):
        qs = Product.objects.all().order_by('-created_at')
        # Prefetch related images to include them in serialized output
        qs = qs.prefetch_related(Prefetch('images', queryset=ProductImage.objects.order_by('created_at')))
        # existing filters (category/search/popular)...
        category = self.request.query_params.get('category')
        popular = self.request.query_params.get('popular')
        search = self.request.query_params.get('search')
        
        if category:
            qs = qs.filter(category__slug=category.lower())
        if popular == 'most':
            qs = qs.annotate(sold=Coalesce(Sum('orderitem__quantity'), 0)).order_by('-sold')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsManager]  

    # Only allow list/create/destroy for nested product routes; optional safety
    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductImage.objects.filter(product_id=product_id).order_by("created_at")

    def create(self, request, product_id=None):
        product = Product.objects.get(id=product_id)

        files = request.FILES.getlist('images')
        if not files:
            return Response({"detail": "No files uploaded"}, status=400)

        if ProductImage.objects.filter(product=product).count() + len(files) > 7:
            return Response({"detail": "Max 7 images allowed"}, status=400)

        created = []
        for img in files:
            obj = ProductImage.objects.create(product=product, image=img)
            created.append(ProductImageSerializer(obj).data)

        return Response(created, status=201)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        qty = serializer.validated_data.get('quantity', 1)

        if qty > product.stock:
            raise serializers.ValidationError("Insufficient stock.")

        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user = request.user
        items = CartItem.objects.filter(user=user).select_related('product')
        if not items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        total = 0
        for it in items:
            if it.quantity > it.product.stock:
                return Response({"detail": f"Product {it.product.name} out of stock or insufficient quantity."}, status=status.HTTP_400_BAD_REQUEST)
            total += it.product.price * it.quantity
            
        promo_code = request.data.get("promo_code")
        discount_amount = 0

        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code, is_active=True)
                
                if promo.expires_at and promo.expires_at < timezone.now():
                    return Response({"detail": "Promo code expired."}, status=400)

                # Apply discount
                if promo.discount_type == "percent":
                    discount_amount = (total * promo.value) / 100
                else:
                    discount_amount = promo.value

            except PromoCode.DoesNotExist:
                return Response({"detail": "Invalid promo code"}, status=400)

        total -= discount_amount
        if total < 0:
            total = 0
        
        order = Order.objects.create(customer=user, total_amount=total)
        order_items = []
        for it in items:
            OrderItem.objects.create(order=order, product=it.product, quantity=it.quantity, price_at_purchase=it.product.price)
            # decrement stock
            it.product.stock = Product.objects.filter(id=it.product.id).update(stock=F('stock') - it.quantity)
        items.delete()
        order.refresh_from_db()
        # Optionally: send confirmation email, payment handling
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    @action(detail=False, methods=['get'])
    def sales_by_product(self, request):
        # returns product id, name, total_sold
        qs = Product.objects.annotate(total_sold=Sum('orderitem__quantity')).order_by('-total_sold')
        # filters
        sort = request.query_params.get('sort')  # most / least
        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category__name__iexact=category)
        if sort == 'least':
            qs = qs.order_by('total_sold')
        data = [{'product_id': p.id, 'name': p.name, 'total_sold': p.total_sold or 0} for p in qs]
        return Response(data)

class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all().order_by('-created_at')
    serializer_class = PromoCodeSerializer
    permission_classes = [IsManager]
