from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from rest_framework.response import Response
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
from rest_framework import status
# Create your views here.
@api_view(["GET","POST"])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.select_related("collection").all( )
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        # print(serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
@api_view(["GET","PUT","DELETE"])
def product_detail(request,id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data) 
    elif request.method== "PUT":
        serializer = ProductSerializer(product,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if product.orderitem_set.filter(product_id=str(id)).exists():
            return Response(
                {"error": "Product cannot be deleted because it is associated with an order item."},
                status=status.HTTP_409_CONFLICT
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET","POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.prefetch_related("product_set").all()
        serializer = CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
@api_view(["GET","PUT","DELETE"])
def collection_detail(request,id):
    collection = get_object_or_404(Collection,pk = id)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method =="PUT":
        serializer = CollectionSerializer(collection,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if collection.product_set.exists():
            return Response(
                {"error": "Collection cannot be deleted because it includes one or more products."},
                status=status.HTTP_409_CONFLICT
            )
        collection.delete()
        return Response( {"message": "Collection deleted successfully."},status=status.HTTP_204_NO_CONTENT)

