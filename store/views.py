from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Cart, Category, Comment, Product
from store.serializers import CartSerializer, CommentSerializer, ProductSerializer,CategorySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    filter_backends =[DjangoFilterBackend,SearchFilter]
    filterset_fields =['category_id','inventory']
    search_fields =['name']
    pagination_class = PageNumberPagination



    
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self,request,pk):
        product=get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk
            )
        if product.order_items.count() > 0:
            return Response({'error':'there is error'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()
    
    def delete(self,request,pk):
        category=get_object_or_404(
            Category.objects.prefetch_related('products'),
            pk=pk
            )
        if category.products.count() > 0:
            return Response({'error':'there is error'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer


    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()
    
    def get_serializer_context(self):
        return {'product_pk':self.kwargs['product_pk']}
    

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    




# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()

#     def delete(self,request,pk):
#         category=get_object_or_404(
#             Category.objects.prefetch_related('products'),
#             pk=pk
#             )
#         if category.products.count() > 0:
#             return Response({'error':'there is error'})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view('GET','POST','DELETE')
# def category_detail(request,pk):
#     category = get_object_or_404(Category,pk=pk)
#     if request.method =='GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if category.products.count()>0:
#             return Response({'error':'there is some product in category'})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
       

# @api_view()
# def category_detail(request, pk):
#     category = get_object_or_404(Category,pk=pk)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)


  

#   class ProductList(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()

#     def get_serializer_context(self):
#         return {'request': self.request}
    
    
     
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()

#     def delete(self,request,pk):
#         product=get_object_or_404(
#             Product.objects.select_related('category'),
#             pk=pk
#             )
#         if product.order_items.count() > 0:
#             return Response({'error':'there is error'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

 