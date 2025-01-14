from django.shortcuts import get_object_or_404
from rest_framework import serializers

from store.models import Cart, Category, Product,Comment
# from django.template.defaultfilters import slugify
from django.utils.text import slugify

DOLLORS_TO_RIALS = 50000

# class categorySerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=255)



class ProductSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=255 ,source='name')
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    unit_price_after_tax = serializers.SerializerMethodField()
  
   
    class Meta:
        model = Product
        fields=['id','title','price','category','unit_price_after_tax','inventory','description']


    def get_unit_price_after_tax(self,product):
        return round(float(product.unit_price)*(1.09),2)
    
    def validate(self, data):
        if len(data['name'])<6:
            raise serializers.ValidationError('is too small')
        return data
    
    def create(self, validated_data):
        product=Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product


class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.IntegerField(source='products.count',read_only=True)

   
    class Meta:
        model = Category
        fields=['id','title','description','num_of_products']

    def get_num_of_products(self, category):
        return category.products.count()


    # id = serializers.IntegerField()
    # name  = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6,decimal_places=2)
    # inventory = serializers.IntegerField()

    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields=['id','name','body']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id,**validated_data)
    

class CartSerializer(serializers.ModelField):
    class Meta:
        model = Cart
        fields =['id','created_at']
    
    # def validate(self, data):
    #     if len(data['name'])<6:
    #         raise serializers.ValidationError('is too small')
    #     return data
    
    # def create(self, validated_data):
    #     comment=Comment(**validated_data)
    #     # comment.slug = slugify(comment.name)
    #     comment.save()
    #     return comment

    