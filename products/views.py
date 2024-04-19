from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product
from rest_framework import status
# Create your views here.

class AddGetProductsView(APIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True ,context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetDeleteUpdateProductView(APIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Product.HTTP_404_NOT_FOUND
        
    def get(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        serializer = self.serializer_class(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)