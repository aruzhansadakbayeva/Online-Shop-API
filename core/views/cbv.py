from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from ..models import Product, CartItem, UserShoppingCart
from ..serializers import ProductSerializer, ProductCreateSerializer, CartItemSerializer, \
    CartItemCreateOrUpdateSerializer, ShoppingCartSerializer


class ProductListAPIView(APIView):
    def get_permissions(self):
        if self.request.method.lower() == 'post':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, request):
        books = Product.objects.all()
        serializer = ProductSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method.lower() == 'get':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = ProductSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = ProductCreateSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    def delete(self, request, book_id):
        book = self.get_object(book_id)
        book.delete()
        return Response({'deleted': True})


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CartItemCreateOrUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class ShoppingCartViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin):
    queryset = UserShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def list(self, request, *args, **kwargs):
        cart = self.queryset.get(owner=self.request.user)
        serializer = self.serializer_class(instance=cart)
        return Response(serializer.data)
