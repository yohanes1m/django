from django.contrib import admin

# Register your models here.
from .models import Product,Collection,Promotion,Customer,Order,OrderItem
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={
        "slug":["title"]
    }
    autocomplete_fields = ["collection"]
    search_fields = ["title"]
    actions = ["clear_inventory"]
    list_display=["id",'title','unit_price','inventory_status',"collection_title",]
    list_editable=["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter =  ["collection","last_updated"]

    def collection_title(self,product):
        return product.collection.title
    @admin.display(ordering="inventory")
    def inventory_status(self,product):
        if product.inventory < 10:
            return "LOW"
        return "OK"
    @admin.action(description="Clear inventory")
    def clear_inventory(self,request,queryset):
        update_count = queryset.update(inventory = 0)
        self.message_user(request,
                          f"{update_count} were updated successfully.")
class CustomProductAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=["membership"]
    list_per_page = 10
    search_fields = ["first_name__istartswith","last_name__istartswith"]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num =1
    max_num = 1
    autocomplete_fields = ["product"]
class OrderAdmin(admin.ModelAdmin):
    list_display = ["placed_at","payment_status","customer_name"]
    list_editable=["payment_status"]
    inlines = [OrderItemInline]
    list_per_page = 10
    list_select_related = ["customer"]
    autocomplete_fields = ["customer"]
   

    def customer_name(self,order):
        return f"{order.customer.first_name} {order.customer.last_name}"
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title","products_count"] 
    @admin.display(ordering="product_count")
    def products_count(self,collection):
          url = reverse("admin:store_product_changelist") + "?" + "{collection__id:str(collection.id)}"
          return  format_html('<a href ="{}">{}</a>',url,collection.products_count)
     
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count("product")
        )

admin.site.register(Product,ProductAdmin)
admin.site.register(Customer,CustomProductAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(Order,OrderAdmin)

