from django.urls import path
from . import views
from rest_framework_nested import routers 




router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='product')
router.register('categories',views.CategoryViewSet,basename='category')
router.register('carts',views.CartViewSet)

products_router = routers.NestedDefaultRouter(router,'products',lookup ='product')
products_router.register('comments',views.CommentViewSet,basename='product-comment')


urlpatterns = router.urls+products_router.urls





# urlpatterns = [

#    path('products/',views.ProductViewSet.as_view(),name='pvs'),
#    path('categories/<int:pk>/',views.CategoryViewSet.as_view(),name='categoryviewset'),
# ]
   # path('products/<int:pk>/',views.ProductDetail.as_view(),name='details'),
   # path('categories/',views.CategoryList.as_view(),name='category'),
