from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,ExpressionWrapper,DecimalField
from django.db.models.aggregates import Count, Min, Max
from store.models import Product,OrderItem,Customer,Collection
from django.db import transaction



# Create your views here.

# def calculate():
#     x= 1
#     y=2
#     return x
@transaction.atomic()
def say(request):


    # get all the product list
    # query_set = Product.objects.all()
    # query_set[0:10:2]


    # to get a single product
    # try:
    #     product  = Product.objects.get(id=0)
    # except ObjectDoesNotExist:
    #     pass 

    # filtering in action 
    # query_set = Product.objects.filter(Q(inventory__lt = 10) | Q(unit_price__lt = 20))
    # query_set = Product.objects.filter(inventory=F("unit_price"))



    # grouping a data
    # query_set = Customer.objects.annotate(
    #     orders_count = Count("order")
    # )


    # sorting 
    # query_set = Product.objects.order_by("-title")[:5]
    

    # selecting fields
    # query_set = Product.objects.values("id","title","collection__title")


    # collecting a related objects
    # query_set = Product.objects.select_related("collection").all()


    # aggregating objects
    # result = Product.objects.aggregate(count = Count("id"),min_price = Min("unit_price"))


    # expressionWrapper example
    query_set = Product.objects.annotate(
        discounted_price = ExpressionWrapper(F("unit_price")*0.8,output_field = DecimalField())
    )

    # exercise to fetch ordered product and sort by title
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values_list("product_id",flat=True).distinct()).order_by("title")
    
 


    # for product in query_set:
    #     print(product)
    # x= calculate()
    # return HttpResponse('Hello world')





    # creating an object 
    # collection = Collection.objects.create(title="video games", featured_product_id=1)
    # collection.id
    



    # updating data 
    # collection = Collection.objects.get(pk=11)
    # collection.title = collection.title
    # collection.featured_product = None
    # collection.save()

    Collection.objects.filter(pk=11).update(featured_product=None)

    return render(request, "hello.html",{"name":"John","result":query_set})