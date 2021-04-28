from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import categories_list, get_category, get_category_products, ProductListAPIView, \
    ProductDetailAPIView, CartItemViewSet, ShoppingCartViewSet

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet)
router.register(r'carts', ShoppingCartViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('categories/', categories_list),
    path('categories/<int:pk>/', get_category),
    path('categories/<int:pk>/products/', get_category_products),
    path('products/', ProductListAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
]
