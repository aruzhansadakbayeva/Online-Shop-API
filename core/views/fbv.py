from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Category, Product
from ..serializers import CategorySerializer, ProductSerializer


@api_view(['GET', 'POST'])
def categories_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def get_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'deleted': True}, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_category_products(request, pk):
    if request.method == 'GET':
        category_products = []
        products = Product.objects.all()
        for product in products:
            if product.category.id == pk:
                category_products.append(product)
        serializer = ProductSerializer(category_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
