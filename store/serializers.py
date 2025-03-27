from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection,Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields= ["id","title","products_count"]
    products_count = serializers.SerializerMethodField(method_name="totalProduct")
    def totalProduct(self,collection):
        return collection.product_set.count()
    
    
      
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","slug","description","inventory","unit_price","price_with_tax","collection"]  
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.5)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length  = 255)
    # price = serializers.DecimalField(decimal_places=2,max_digits=6,source="unit_price")
    # collection = serializers.StringRelatedField(
    #     queryset = Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id","name","date","description","product"]