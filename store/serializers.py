from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection


class CollectionSerializer(serializers.ModelSerializer):
   class Meta:
       model = Collection
       fields= ["id","title"]
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","unit_price","price_with_tax","collection"]  
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length  = 255)
    # price = serializers.DecimalField(decimal_places=2,max_digits=6,source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = serializers.StringRelatedField(
    #     queryset = Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()


    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.5)
