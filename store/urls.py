from rest_framework import routers
from .views import (
    ProductViewSet, CategoryViewSet, CartViewSet, WishlistViewSet,
    ReportViewSet, PromoCodeViewSet, ProductImageViewSet, RegisterView, CreateManagerView
)
from django.urls import path, include

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('cart', CartViewSet, basename='cart')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('promocodes', PromoCodeViewSet)

report_list = ReportViewSet.as_view({'get': 'sales_by_product'})

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/create-manager/', CreateManagerView.as_view(), name='create-manager'),
    
    # HYBRID ROUTES (slug + id)
    path(
        "products/<slug:slug>/<int:pk>/",
        ProductViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="product-details"
    ),

    path(
        "categories/<slug:slug>/<int:pk>/",
        CategoryViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="category-details"
    ),

    # DEFAULT ROUTER
    path("", include(router.urls)),
    
    path('reports/sales-by-product/', report_list, name='sales-by-product'),

    # PRODUCT IMAGES (Nested Routes)
    path(
        'products/<int:product_id>/images/',
        ProductImageViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='product-images-list-create'
    ),
    path(
        'products/<int:product_id>/images/<int:pk>/',
        ProductImageViewSet.as_view({'delete': 'destroy','patch': 'partial_update'}),
        name='product-images-delete'
    ),
]
