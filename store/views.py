from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.db.models import Count
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from .models import Product,Collection,Review
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
from rest_framework import status
from .filters import ProductFilter
from .pagination import DefaultPagination
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    ordering_fields = ["unit_price","title"]
    search_fields = ["title","description"]
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    lookup_field = "id"
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        print("->",product.orderitem)
        if product.orderitem.exists():
            return Response(
                {"error": "Product cannot be deleted because it is associated with an order item."},
                status=status.HTTP_409_CONFLICT
            )
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # def get(self,request):
    #     queryset = Product.objects.select_related("collection").all( )
    #     serializer = ProductSerializer(queryset,many=True)
    #     return Response(serializer.data)
    # def post(self,request):
    #     serializer = ProductSerializer(data = request.data)
    #     serializer.is_valid(raise_exception= True)
    #     serializer.save()
    #     # print(serializer.validated_data)
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product
#     serializer_class = ProductSerializer

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(
            products_count = Count("product")).all()
    serializer_class= CollectionSerializer
    lookup_field = "id"
    def delete(self, request, id):
         collection = get_object_or_404(Collection,pk = id)
         if collection.product_set.exists():
            return Response(
                {"error": "Collection cannot be deleted because it includes one or more products."},
                status=status.HTTP_409_CONFLICT)
         collection.delete()
         return Response( {"message": "Collection deleted successfully."},status=status.HTTP_204_NO_CONTENT)
# @api_view(["GET","POST"])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.prefetch_related("product_set").all()
#         serializer = CollectionSerializer(queryset,many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection
#     serializer_class = CollectionSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
