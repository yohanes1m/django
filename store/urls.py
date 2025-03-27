from django.urls import path,include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("product",views.ProductViewSet,basename="product")
router.register("collection",views.CollectionViewSet)

review_router = routers.NestedDefaultRouter(router,"product",lookup = "product")
review_router.register("review",views.ReviewViewSet,basename="product-review")

# print(router.urls)
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(review_router.urls)),
]

# urlpatterns = [
#     path("product/",views.ProductViewSet.as_view()),
#     path("product/<int:id>/",views.ProductViewSet.as_view()),
#     path("collection/",views.CollectionViewSet.as_view()),
#     path("collection/<int:id>/",views.CollectionViewSet.as_view())
# ]